document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formProducto');
    const nombre = document.getElementById('nombre');
    const categoria = document.getElementById('categoria');
    const precio = document.getElementById('precio');
    const lista = document.getElementById('listaProductos');
    const contador = document.getElementById('contador');
    const vacio = document.getElementById('vacio');
    const errNombre = document.getElementById('errNombre');
    const errCategoria = document.getElementById('errCategoria');
    let total = 0;

    function act() {
        contador.textContent = total;
        if (total === 0) {
            if (!document.getElementById('vacio')) {
                let p = document.createElement('p');
                p.id = 'vacio';
                p.className = 'text-muted text-center';
                p.textContent = 'No hay productos registrados';
                lista.appendChild(p);
            }
        } else {
            let p = document.getElementById('vacio');
            if (p) p.remove();
        }
    }

    function crear(n, c, p) {
        let col = document.createElement('div');
        col.className = 'col-md-4 col-sm-6 mb-3';
        let card = document.createElement('div');
        card.className = 'card h-100';
        let body = document.createElement('div');
        body.className = 'card-body';
        let h5 = document.createElement('h5');
        h5.className = 'card-title text-primary';
        h5.textContent = n;
        let cat = document.createElement('p');
        cat.className = 'card-text small';
        cat.innerHTML = '<strong>Categoria:</strong> ' + c;
        let prec = document.createElement('p');
        prec.className = 'card-text';
        prec.textContent = p > 0 ? 'Precio: $' + parseFloat(p).toFixed(2) : 'Precio: No especificado';
        let btn = document.createElement('button');
        btn.className = 'btn btn-danger btn-sm mt-2';
        btn.textContent = 'Eliminar';
        btn.addEventListener('click', function() {
            if (confirm('Eliminar ' + n + '?')) {
                col.remove();
                total--;
                act();
            }
        });
        body.appendChild(h5);
        body.appendChild(cat);
        body.appendChild(prec);
        body.appendChild(btn);
        card.appendChild(body);
        col.appendChild(card);
        return col;
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        let valido = true;
        if (nombre.value.trim() === '') { errNombre.style.display = 'block'; nombre.classList.add('is-invalid'); valido = false; } 
        else { errNombre.style.display = 'none'; nombre.classList.remove('is-invalid'); }
        if (categoria.value === '') { errCategoria.style.display = 'block'; categoria.classList.add('is-invalid'); valido = false; } 
        else { errCategoria.style.display = 'none'; categoria.classList.remove('is-invalid'); }
        if (!valido) return;
        lista.appendChild(crear(nombre.value.trim(), categoria.value, parseFloat(precio.value) || 0));
        total++;
        act();
        form.reset();
        nombre.classList.remove('is-invalid');
        categoria.classList.remove('is-invalid');
        nombre.focus();
    });

    nombre.addEventListener('input', function() {
        if (this.value.trim() !== '') { errNombre.style.display = 'none'; this.classList.remove('is-invalid'); }
    });
    categoria.addEventListener('change', function() {
        if (this.value !== '') { errCategoria.style.display = 'none'; this.classList.remove('is-invalid'); }
    });
    act();
});