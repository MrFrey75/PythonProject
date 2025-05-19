from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Board, Page

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
        content = request.form['page_content']
        order = request.form.get('order', 0)
        new_page = Page(board_id=board.id, content=content, order=int(order))
        db.session.add(new_page)
        db.session.commit()
        flash("Page added!")
        return redirect(url_for('main.edit_board', board_id=board.id))
    return render_template('edit_board.html', board=board)

@main.route('/admin/page/<int:page_id>/edit', methods=['GET', 'POST'])
def edit_page(page_id):
    page = Page.query.get_or_404(page_id)
    if request.method == 'POST':
        page.content = request.form['page_content']
        page.order = int(request.form['order'])
        db.session.commit()
        flash("Page updated!")
        return redirect(url_for('main.edit_board', board_id=page.board_id))
    return render_template('edit_page.html', page=page)

@main.route('/admin/page/<int:page_id>/delete', methods=['POST'])
def delete_page(page_id):
    page = Page.query.get_or_404(page_id)
    board_id = page.board_id
    db.session.delete(page)
    db.session.commit()
    flash("Page deleted!")
    return redirect(url_for('main.edit_board', board_id=board_id))
