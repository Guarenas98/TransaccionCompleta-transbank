from flask import render_template, request, Flask
from transbank.transaccion_completa.transaction import Transaction
from datetime import datetime as dt
from datetime import timedelta


app = Flask(__name__)  # server desde el modulo python actual


#++++++++++++++Transaccion completa++++++++++++++++++++++++

@app.route("/")
@app.route('/create', methods=['GET'])
def show_create():
    return render_template('transaccion_completa/create.html', dt=dt, timedelta=timedelta)


@app.route('/create', methods=['POST'])
def send_create():
    buy_order = request.form.get('buy_order')
    session_id = request.form.get('session_id')
    amount = request.form.get('amount')
    card_number = request.form.get('card_number')
    cvv = request.form.get('cvv')
    card_expiration_date = request.form.get('card_expiration_date')

    resp = Transaction.create(
        buy_order=buy_order, session_id=session_id, amount=amount,
        card_number=card_number, cvv=cvv, card_expiration_date=card_expiration_date
    )

    return render_template('transaccion_completa/created.html', resp=resp, req=request.form.values, dt=dt)


@app.route('/installments', methods=['POST'])
def installments():
    req = request.form
    token = request.form.get('token')
    installments_number = request.form.get('installments_number')
    resp = Transaction.installments(token=token, installments_number=installments_number)
    return render_template('transaccion_completa/installments.html', req=req, resp=resp)


@app.route('/commit', methods=['POST'])
def commit():
    req = request.form
    token = request.form.get('token')
    id_query_installments = request.form.get('id_query_installments')
    deferred_period_index = request.form.get('deferred_period_index')
    grace_period = request.form.get('grace_period') != 'false'

    resp = Transaction.commit(token=token,
                              id_query_installments=id_query_installments,
                              deferred_period_index=deferred_period_index,
                              grace_period=grace_period)
    return render_template('transaccion_completa/transaction_committed.html', req=req, resp=resp)


@app.route('/status/<token>', methods=['GET'])
def status(token):
    req = request.form
    resp = Transaction.status(token=token)
    return render_template('transaccion_completa/transaction_status.html', req=req, resp=resp)


@app.route('/refund', methods=['POST'])
def refund():
    req = request.form
    token = req.get('token')
    amount = req.get('amount')
    resp = Transaction.refund(token=token, amount=amount)
    return render_template('transaccion_completa/transaction_refunded.html', req=req, resp=resp)



if __name__ == "__main__":
    app.run(debug = True ,port = 8081)  # ejecutar servidor y esperar peticiones