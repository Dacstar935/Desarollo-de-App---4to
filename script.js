document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formProducto');
    const n = document.getElementById('nombre');
    const c = document.getElementById('categoria');
    const p = document.getElementById('precio');
    const d = document.getElementById('descripcion');
    const lista = document.getElementById('listaProductos');
    const contador = document.getElementById('contador');
    const mensajeExito = document.getElementById('mensajeExito');

    const errN = document.getElementById('errNombre');
    const errC = document.getElementById('errCategoria');
    const errP = document.getElementById('errPrecio');
    const errD = document.getElementById('errDescripcion');
    const okN = document.getElementById('okNombre');
    const okC = document.getElementById('okCategoria');
    const okP = document.getElementById('okPrecio');
    const okD = document.getElementById('okDescripcion');

    let total = 0;

    function val(campo, error, ok, condicion) {
        if (condicion) {
            campo.classList.remove('is-invalid');
            campo.classList.add('is-valid');
            error.style.display = 'none';
            if (ok) ok.style.display = 'block';
            return true;
        } else {
            campo.classList.remove('is-valid');
            campo.classList.add('is-invalid');
            error.style.display = 'block';
            if (ok) ok.style.display = 'none';
            return false;
        }
    }

    function validarNombre() {
        return val(n, errN, okN, n.value.trim().length >= 3);
    }
    function validarCategoria() {
        return val(c, errC, okC, c.value !== '');
    }
    function validarPrecio() {
        return val(p, errP, okP, p.value === '' || parseFloat(p.value) >= 0);
    }
    function validarDescripcion() {
        return val(d, errD, okD, d.value.trim().length >= 10);
    }
    function validarTodo() {
        return validarNombre() && validarCategoria() && validarPrecio() && validarDescripcion();
    }

    function act() {
        contador.textContent = total;
        if (total === 0) {
            if (!document.getElementById('vacio')) {
                let p = document.createElement('p');
                p.id = 'vacio';
                p.className = 'text-muted text-center';
                p.textContent = 'No hay productos';
                lista.appendChild(p);
            }
        } else {
            let p = document.getElementById('vacio');
            if (p) p.remove();
        }
    }

    function crear(nom, cat, pre, des) {
        let col = document.createElement('div');
        col.className = 'col-md-4 col-sm-6 mb-3';
        let card = document.createElement('div');
        card.className = 'card h-100';
        let body = document.createElement('div');
        body.className = 'card-body';
        let h5 = document.createElement('h5');
        h5.className = 'card-title text-primary';
        h5.textContent = nom;
        let info = document.createElement('p');
        info.className = 'card-text small';
        info.innerHTML = '<strong>Categoria:</strong> ' + cat + '<br><strong>Descripcion:</strong> ' + des;
        let prec = document.createElement('p');
        prec.className = 'card-text';
        prec.textContent = pre > 0 ? 'Precio: $' + parseFloat(pre).toFixed(2) : 'Precio: N/E';
        let btn = document.createElement('button');
        btn.className = 'btn btn-danger btn-sm mt-2';
        btn.textContent = 'Eliminar';
        btn.addEventListener('click', function() {
            if (confirm('Eliminar "' + nom + '"?')) { col.remove(); total--; act(); }
        });
        body.appendChild(h5);
        body.appendChild(info);
        body.appendChild(prec);
        body.appendChild(btn);
        card.appendChild(body);
        col.appendChild(card);
        return col;
    }

    n.addEventListener('input', validarNombre);
    n.addEventListener('blur', validarNombre);
    c.addEventListener('change', validarCategoria);
    c.addEventListener('blur', validarCategoria);
    p.addEventListener('input', validarPrecio);
    p.addEventListener('blur', validarPrecio);
    d.addEventListener('input', validarDescripcion);
    d.addEventListener('blur', validarDescripcion);

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        if (!validarTodo()) {
            let alerta = document.createElement('div');
            alerta.className = 'alert alert-danger';
            alerta.textContent = 'Corrige los errores';
            form.prepend(alerta);
            setTimeout(function() { alerta.remove(); }, 3000);
            return;
        }
        lista.appendChild(crear(n.value.trim(), c.value, parseFloat(p.value) || 0, d.value.trim()));
        total++;
        act();
        mensajeExito.style.display = 'block';
        setTimeout(function() { mensajeExito.style.display = 'none'; }, 3000);
        form.reset();
        [n, c, p, d].forEach(function(campo) { campo.classList.remove('is-valid', 'is-invalid'); });
        [okN, okC, okP, okD].forEach(function(msg) { msg.style.display = 'none'; });
        [errN, errC, errP, errD].forEach(function(msg) { msg.style.display = 'none'; });
        n.focus();
    });

    act();
});