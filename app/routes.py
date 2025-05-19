from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Board, Page, Section, page_sections

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return redirect('/admin')


@main.route('/board/<board_id>')
def show_board(board_id):
    board = Board.query.get_or_404(board_id)
    pages = sorted(board.pages, key=lambda p: p.order)
    return render_template('board.html', board=board, pages=pages)


@main.route('/admin', methods=['GET', 'POST'])
def admin():
    boards = Board.query.all()
    if request.method == 'POST':
        name = request.form['board_name']
        new_board = Board(name=name)
        db.session.add(new_board)
        db.session.commit()
        return redirect(url_for('main.admin'))
    return render_template('admin.html', boards=boards)


@main.route('/admin/board/<board_id>', methods=['GET', 'POST'])
def edit_board(board_id):
    board = Board.query.get_or_404(board_id)
    if request.method == 'POST':
        name = request.form.get('page_name', 'Untitled Page')
        order = request.form.get('order', 0)
        new_page = Page(name=name, board_id=board.id, order=int(order))
        db.session.add(new_page)
        db.session.commit()
        flash("Page added!")
        return redirect(url_for('main.edit_board', board_id=board.id))
    return render_template('edit_board.html', board=board)


@main.route('/admin/page/<int:page_id>/edit', methods=['GET', 'POST'])
def edit_page(page_id):
    page = Page.query.get_or_404(page_id)
    if request.method == 'POST':
        page.order = int(request.form['order'])
        db.session.execute(page_sections.delete().where(page_sections.c.page_id == page.id))

        section_ids = request.form.getlist('section_ids')
        for idx, section_id in enumerate(section_ids):
            db.session.execute(page_sections.insert().values(
                page_id=page.id,
                section_id=int(section_id),
                position=idx
            ))

        db.session.commit()
        flash("Page updated!")
        return redirect(url_for('main.edit_board', board_id=page.board_id))

    all_sections = Section.query.all()
    current_section_ids = [s.id for s in page.sections]
    return render_template(
        'edit_page.html',
        page=page,
        available_sections=all_sections,
        current_section_ids=current_section_ids
    )


@main.route('/admin/page/<int:page_id>/delete', methods=['POST'])
def delete_page(page_id):
    page = Page.query.get_or_404(page_id)
    board_id = page.board_id
    db.session.execute(page_sections.delete().where(page_sections.c.page_id == page.id))
    db.session.delete(page)
    db.session.commit()
    flash("Page deleted!")
    return redirect(url_for('main.edit_board', board_id=board_id))


@main.route('/admin/sections')
def list_sections():
    sections = Section.query.all()
    return render_template('sections.html', sections=sections)


@main.route('/admin/section/new', methods=['GET', 'POST'])
def create_section():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        section = Section(title=title, content=content)
        db.session.add(section)
        db.session.commit()
        return redirect(url_for('main.list_sections'))
    return render_template('section_form.html', section=None)


@main.route('/admin/section/<int:section_id>', methods=['GET', 'POST'])
def edit_section(section_id):
    section = Section.query.get_or_404(section_id)
    if request.method == 'POST':
        section.title = request.form['title']
        section.content = request.form['content']
        db.session.commit()
        return redirect(url_for('main.list_sections'))
    return render_template('section_form.html', section=section)


@main.route('/admin/reset-db', methods=['POST'])
def reset_db():
    db.drop_all()
    db.create_all()

    from .seed_demo import seed_demo_data
    seed_demo_data()

    flash("✅ Database has been reset and seeded with demo data.")
    return redirect(url_for('main.admin'))
