import os
from flask import Flask, render_template, request, redirect
from database import conectar_bd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar_proveedor', methods=['GET', 'POST'])
def agregar_proveedor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO proveedores (nombre, email, telefono) VALUES (?, ?, ?)', (nombre, email, telefono))
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template('agregar_proveedor.html')

@app.route('/editar_proveedor/<int:proveedor_id>', methods=['GET', 'POST'])
def editar_proveedor(proveedor_id):
    conn = conectar_bd()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form.get('direccion')  # Si usas dirección en el formulario
        telefono = request.form.get('telefono')
        email = request.form.get('email')

        cursor.execute('UPDATE proveedores SET nombre=?, direccion=?, telefono=?, email=? WHERE id=?',
                       (nombre, direccion, telefono, email, proveedor_id))
        conn.commit()
        conn.close()
        return redirect('/listar_proveedores')

    # Si es un GET, recupera los datos del proveedor para rellenar el formulario
    cursor.execute('SELECT * FROM proveedores WHERE id=?', (proveedor_id,))
    proveedor = cursor.fetchone()
    conn.close()

    return render_template('editar_proveedor.html', proveedor=proveedor)

@app.route('/eliminar_proveedor/<int:proveedor_id>', methods=['POST'])
def eliminar_proveedor(proveedor_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM proveedores WHERE id = ?', (proveedor_id,))
    conn.commit()
    conn.close()
    
    return redirect('/listar_proveedores')

@app.route('/listar_proveedores')
def listar_proveedores():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM proveedores')
    proveedores = cursor.fetchall()
    conn.close()
    return render_template('listar_proveedores.html', proveedores=proveedores)

@app.route('/agregar_deuda', methods=['GET', 'POST'])
def agregar_deuda():
    if request.method == 'POST':
        proveedor_id = request.form['proveedor_id']
        monto = request.form['monto']
        fecha_vencimiento = request.form['fecha_vencimiento']

        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO deudas (proveedor_id, monto, fecha_vencimiento) VALUES (?, ?, ?)', (proveedor_id, monto, fecha_vencimiento))
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template('agregar_deuda.html')

@app.route('/listar_deudas')
def listar_deudas():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM deudas')
    deudas = cursor.fetchall()
    conn.close()
    return render_template('listar_deudas.html', deudas=deudas)

@app.route('/editar_deuda/<int:deuda_id>', methods=['GET', 'POST'])
def editar_deuda(deuda_id):
    conn = conectar_bd()
    cursor = conn.cursor()

    if request.method == 'POST':
        proveedor_id = request.form['proveedor_id']
        monto = request.form['monto']
        fecha_vencimiento = request.form['fecha_vencimiento']

        cursor.execute('UPDATE deudas SET proveedor_id=?, monto=?, fecha_vencimiento=? WHERE id=?',
                       (proveedor_id, monto, fecha_vencimiento, deuda_id))
        conn.commit()
        conn.close()
        return redirect('/listar_deudas')

    cursor.execute('SELECT * FROM deudas WHERE id=?', (deuda_id,))
    deuda = cursor.fetchone()
    conn.close()
    return render_template('editar_deuda.html', deuda=deuda)

@app.route('/eliminar_deuda/<int:deuda_id>', methods=['POST'])
def eliminar_deuda(deuda_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM deudas WHERE id = ?', (deuda_id,))
    conn.commit()
    conn.close()
    
    return redirect('/listar_deudas')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

UPLOAD_FOLDER = '\\Users\\Prueba\\Desktop\\Cuentas por pagar\\Cuentas por pagar\\static\\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/agregar_factura', methods=['GET', 'POST'])
def agregar_factura():
    if request.method == 'POST':
        proveedor_id = request.form['proveedor_id']
        monto = request.form['monto']
        fecha = request.form['fecha']
        fecha_vencimiento = request.form['fecha_vencimiento']
        condiciones_pago = request.form['condiciones_pago']

        # Manejo de archivos subidos
        archivo = request.files['archivo']
        if archivo:
            archivo_path = os.path.join(app.config['UPLOAD_FOLDER'], archivo.filename)
            archivo.save(archivo_path)
        else:
            archivo_path = None

        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO facturas (proveedor_id, monto, fecha, fecha_vencimiento, condiciones_pago, archivo) VALUES (?, ?, ?, ?, ?, ?)', (proveedor_id, monto, fecha, fecha_vencimiento, condiciones_pago, archivo_path))
        conn.commit()
        conn.close()
        return redirect('/listar_facturas')

    return render_template('agregar_factura.html')

@app.route('/editar_factura/<int:factura_id>', methods=['GET', 'POST'])
def editar_factura(factura_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    if request.method == 'POST':
        proveedor_id = request.form['proveedor_id']
        monto = request.form['monto']
        fecha = request.form['fecha']
        fecha_vencimiento = request.form['fecha_vencimiento']
        condiciones_pago = request.form['condiciones_pago']

        # Manejo de archivos subidos
        archivo = request.files['archivo']
        if archivo:
            archivo_path = f'static/uploads/{archivo.filename}'
            archivo.save(archivo_path)
        else:
            archivo_path = None

        cursor.execute('UPDATE facturas SET proveedor_id=?, monto=?, fecha=?, fecha_vencimiento=?, condiciones_pago=?, archivo=? WHERE id=?',
                       (proveedor_id, monto, fecha, fecha_vencimiento, condiciones_pago, archivo_path, factura_id))
        conn.commit()
        conn.close()
        return redirect('/listar_facturas')

    cursor.execute('SELECT * FROM facturas WHERE id=?', (factura_id,))
    factura = cursor.fetchone()
    conn.close()
    return render_template('editar_factura.html', factura=factura)

@app.route('/eliminar_factura/<int:factura_id>', methods=['POST'])
def eliminar_factura(factura_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM facturas WHERE id = ?', (factura_id,))
    conn.commit()
    conn.close()
    
    return redirect('/listar_facturas')

@app.route('/listar_facturas')
def listar_facturas():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM facturas')
    facturas = cursor.fetchall()
    conn.close()
    return render_template('listar_facturas.html', facturas=facturas)

@app.route('/registrar_pago', methods=['GET', 'POST'])
def registrar_pago():
    if request.method == 'POST':
        factura_id = request.form['factura_id']
        monto = request.form['monto']
        fecha = request.form['fecha']
        metodo_pago = request.form['metodo_pago']

        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO pagos (factura_id, monto, fecha, metodo_pago) VALUES (?, ?, ?, ?)', (factura_id, monto, fecha, metodo_pago))
        conn.commit()
        conn.close()
        return redirect('/listar_pagos')

    return render_template('registrar_pago.html')

@app.route('/listar_pagos')
def listar_pagos():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pagos')
    pagos = cursor.fetchall()
    conn.close()
    return render_template('listar_pagos.html', pagos=pagos)

@app.route('/editar_pago/<int:pago_id>', methods=['GET', 'POST'])
def editar_pago(pago_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        factura_id = request.form['factura_id']
        monto = request.form['monto']
        fecha = request.form['fecha']
        metodo_pago = request.form['metodo_pago']

        cursor.execute('UPDATE pagos SET factura_id=?, monto=?, fecha=?, metodo_pago=? WHERE id=?',
                       (factura_id, monto, fecha, metodo_pago, pago_id))
        conn.commit()
        conn.close()
        return redirect('/listar_pagos')

    cursor.execute('SELECT * FROM pagos WHERE id=?', (pago_id,))
    pago = cursor.fetchone()
    conn.close()
    return render_template('editar_pago.html', pago=pago)

@app.route('/eliminar_pago/<int:pago_id>', methods=['POST'])
def eliminar_pago(pago_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM pagos WHERE id = ?', (pago_id,))
    conn.commit()
    conn.close()
    
    return redirect('/listar_pagos')

@app.route('/reportes')
def reportes():
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM facturas')
    facturas = cursor.fetchall()

    cursor.execute('SELECT * FROM pagos')
    pagos = cursor.fetchall()

    conn.close()
    return render_template('reportes.html', facturas=facturas, pagos=pagos)


if __name__ == '__main__':
    app.run(debug=True)
