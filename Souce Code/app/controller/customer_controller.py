@app.route('/customer')
@login_required
def customer():

    cur = mysql.connection.cursor()
    cur.execute("select * from customer")
    customers = cur.fetchall()
    # print(customers)
    return render_template('customer_list.html', customers = customers)

@app.route('/customer_addnew', methods=['GET', 'POST'])
@login_required
@admin_required
def customer_addnew():
    if request.method == "POST":


        details = request.form
        username = details['username']
        email = details['email']
        mobile = details['mobile']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO customer(username, email, mobile) VALUES (%s, %s , %s)", (username, email,mobile))
        mysql.connection.commit()
        cur.close()
        # return 'success'
        return redirect('/customer')

    return render_template('customer_add.html')

@app.route('/customer_edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def customer_edit(id):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("select * from customer where id ="+str(id))
        customers = cur.fetchall()

        return render_template('customer_edit.html', customers = customers)

@app.route('/customer_update/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def customer_update(id):

    details = request.form
    if request.method == "POST":

        if 'update_sub' in request.form:

            username = details['username']
            email = details['email']
            mobile = details['mobile']
            cur = mysql.connection.cursor()
            cur.execute("Update customer set username ='"+username+"',email = '"+email+"' , mobile = '"+mobile+"' where id="+str(id))
            mysql.connection.commit()
            cur.close()
            # return 'success'
            return redirect('/customer')

        elif 'email_sub' in request.form:

            # email = details['email']
            noti.send_notification_email("test",details['email'],"test clause")



        elif 'SMS_sub' in request.form:

            mobile = details['mobile']
            noti.send_SMS("test",details['mobile'],"")
            print("===========Test SMS")


    cur = mysql.connection.cursor()
    cur.execute("select * from customer where id ="+str(id))
    customers = cur.fetchall()

    return render_template('customer_edit.html', customers = customers)
    # return redirect("/customer_update/"+str(id))

@app.route('/customer_delete/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def customer_delete(id):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("delete from customer where id ="+str(id))
        mysql.connection.commit()
        cur.close()
        # return 'success'
        return redirect('/customer')