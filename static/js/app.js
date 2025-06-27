document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const metodoForm = document.getElementById('metodoForm');
    const metodoSelect = document.getElementById('metodo');
    const gxContainer = document.getElementById('gx-container');
    const x1Container = document.getElementById('x1-container');
    const resultadosSection = document.getElementById('resultados');
    const resultadoTitulo = document.getElementById('resultado-titulo');
    const resultadoTexto = document.getElementById('resultado-texto');
    const tablaResultados = document.getElementById('tabla-resultados');
    const exportarExcelBtn = document.getElementById('exportar-excel');
    const exportarPdfBtn = document.getElementById('exportar-pdf');
    
    // Gráficos
    let errorChart = null;
    let funcionChart = null;
    
    // Datos actuales
    let currentData = null;
    let currentMethod = null;
    let currentFunction = null;
    
    // Manejar cambios en el método seleccionado
    metodoSelect.addEventListener('change', function() {
        gxContainer.style.display = this.value === 'punto_fijo' ? 'block' : 'none';
        x1Container.style.display = this.value === 'secante' ? 'block' : 'none';
    });
    
    // Enviar formulario
    metodoForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Obtener datos del formulario
        const metodo = metodoSelect.value;
        const funcion = document.getElementById('funcion').value;
        const funcion_g = metodo === 'punto_fijo' ? document.getElementById('funcion_g').value : null;
        const x0 = parseFloat(document.getElementById('x0').value);
        const x1 = metodo === 'secante' ? parseFloat(document.getElementById('x1').value) : null;
        const tolerancia = parseFloat(document.getElementById('tolerancia').value);
        const max_iter = parseInt(document.getElementById('max_iter').value);
        
        // Validaciones
        if (!metodo || !funcion || isNaN(x0) || isNaN(tolerancia) || isNaN(max_iter)) {
            alert('Por favor complete todos los campos requeridos');
            return;
        }
        
        if (metodo === 'punto_fijo' && !funcion_g) {
            alert('Para el método de Punto Fijo debe ingresar la función g(x)');
            return;
        }
        
        if (metodo === 'secante' && isNaN(x1)) {
            alert('Para el método de la Secante debe ingresar x1');
            return;
        }
        
        // Preparar datos para enviar al backend
        const data = {
            metodo: metodo,
            funcion: funcion,
            x0: x0,
            tolerancia: tolerancia,
            max_iter: max_iter
        };
        
        if (metodo === 'punto_fijo') data.funcion_g = funcion_g;
        if (metodo === 'secante') data.x1 = x1;
        
        // Mostrar carga
        resultadoTitulo.textContent = 'Calculando...';
        resultadoTexto.textContent = '';
        resultadosSection.style.display = 'block';
        
        // Llamar al backend
        fetch('/calcular', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Guardar datos actuales
            currentData = data.resultados;
            currentMethod = metodo;
            currentFunction = funcion;
            
            // Mostrar resultados
            mostrarResultados(data, metodo);
            
            // Crear gráficos
            crearGraficos(data, metodo);
        })
        .catch(error => {
            console.error('Error:', error);
            resultadoTitulo.textContent = 'Error';
            resultadoTexto.textContent = error.message;
        });
    });
    
    // Función para mostrar resultados en la tabla
    function mostrarResultados(data, metodo) {
        // Configurar título y texto de resultados
        const nombresMetodos = {
            'newton': 'Newton-Raphson',
            'punto_fijo': 'Punto Fijo',
            'secante': 'Secante'
        };
        
        resultadoTitulo.textContent = `Método de ${nombresMetodos[metodo]}`;
        resultadoTexto.textContent = `Raíz aproximada: ${data.raiz.toFixed(6)} | Iteraciones: ${data.iteraciones}`;
        
        // Configurar columnas de la tabla según el método
        let columnas = [];
        
        switch(metodo) {
            case 'newton':
                columnas = ['Iteración', 'X_i-1', 'f(X_i-1)', "f'(X_i-1)", 'X_i', 'Error'];
                break;
            case 'secante':
                columnas = ['Iteración', 'X_i-1', 'X_i', 'f(X_i-1)', 'f(X_i)', 'X_i+1', 'f(X_i+1)', 'Error'];
                break;
            case 'punto_fijo':
                columnas = ['Iteración', 'X_n', 'X_n+1', 'Error'];
                break;
        }
        
        // Limpiar tabla
        tablaResultados.innerHTML = '';
        
        // Crear encabezados
        const thead = document.createElement('thead');
        thead.className = 'table-dark';
        const headerRow = document.createElement('tr');
        
        columnas.forEach(col => {
            const th = document.createElement('th');
            th.textContent = col;
            headerRow.appendChild(th);
        });
        
        thead.appendChild(headerRow);
        tablaResultados.appendChild(thead);
        
        // Crear cuerpo de la tabla
        const tbody = document.createElement('tbody');
        
        data.resultados.forEach(fila => {
            const tr = document.createElement('tr');
            
            // Convertir fila a array si es necesario (dependiendo del método)
            let valores = [];
            if (metodo === 'newton') {
                valores = [fila.iter, fila.x, fila.fx, fila.dfx, fila.x_next, fila.error];
            } else if (metodo === 'secante') {
                valores = [fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7]];
            } else if (metodo === 'punto_fijo') {
                valores = [fila[0], fila[1], fila[2], fila[3]];
            }
            
            valores.forEach(valor => {
                const td = document.createElement('td');
                td.textContent = typeof valor === 'number' ? valor.toFixed(6) : valor;
                tr.appendChild(td);
            });
            
            tbody.appendChild(tr);
        });
        
        tablaResultados.appendChild(tbody);
        
        // Mostrar sección de resultados con animación
        resultadosSection.classList.add('fade-in');
    }
    
    // Función para crear gráficos
    function crearGraficos(data, metodo) {
        const ctxError = document.getElementById('grafica-error').getContext('2d');
        const ctxFuncion = document.getElementById('grafica-funcion').getContext('2d');
        
        // Destruir gráficos anteriores si existen
        if (errorChart) errorChart.destroy();
        if (funcionChart) funcionChart.destroy();
        
        // Preparar datos para gráfico de error
        const iteraciones = data.resultados.map((_, i) => i + 1);
        const errores = data.resultados.map(fila => {
            if (metodo === 'newton') return fila.error;
            if (metodo === 'secante') return fila[7];
            if (metodo === 'punto_fijo') return fila[3];
        });
        
        // Gráfico de error
        errorChart = new Chart(ctxError, {
            type: 'line',
            data: {
                labels: iteraciones,
                datasets: [{
                    label: 'Error por iteración',
                    data: errores,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Convergencia del Error'
                    }
                },
                scales: {
                    y: {
                        type: 'logarithmic',
                        title: {
                            display: true,
                            text: 'Error (escala logarítmica)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Iteración'
                        }
                    }
                }
            }
        });
        
        // Gráfico de función (simplificado)
        // Para un gráfico real necesitaríamos evaluar la función en varios puntos
        const puntosX = Array.from({length: 100}, (_, i) => data.raiz - 2 + i * 0.04);
        
        // Evaluar la función (esto es una simulación, en la práctica necesitarías un parser matemático)
        // En una implementación real, esto se haría en el backend
        const puntosY = puntosX.map(x => {
            try {
                // Esto es una simulación muy básica - en producción usarías un parser matemático real
                const expr = currentFunction.replace(/x/g, `(${x})`).replace(/\^/g, '**');
                return eval(expr);
            } catch {
                return NaN;
            }
        });
        
        funcionChart = new Chart(ctxFuncion, {
            type: 'line',
            data: {
                labels: puntosX.map(x => x.toFixed(2)),
                datasets: [{
                    label: 'f(x)',
                    data: puntosY,
                    borderColor: 'rgba(153, 102, 255, 1)',
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    tension: 0.1
                }, {
                    label: 'Raíz aproximada',
                    data: puntosX.map(x => x === data.raiz ? 0 : null),
                    pointBackgroundColor: 'red',
                    pointRadius: 5,
                    showLine: false
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Gráfico de la Función'
                    }
                },
                scales: {
                    y: {
                        title: {
                            display: true,
                            text: 'f(x)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'x'
                        }
                    }
                }
            }
        });
    }
    
    // Exportar a Excel
    exportarExcelBtn.addEventListener('click', function() {
        if (!currentData) {
            alert('No hay datos para exportar');
            return;
        }
        
        // Preparar datos para exportación
        let datosExportar = [];
        let columnas = [];
        
        switch(currentMethod) {
            case 'newton':
                columnas = ['Iteración', 'X_i-1', 'f(X_i-1)', "f'(X_i-1)", 'X_i', 'Error'];
                datosExportar = currentData.map(fila => [
                    fila.iter,
                    fila.x,
                    fila.fx,
                    fila.dfx,
                    fila.x_next,
                    fila.error
                ]);
                break;
            case 'secante':
                columnas = ['Iteración', 'X_i-1', 'X_i', 'f(X_i-1)', 'f(X_i)', 'X_i+1', 'f(X_i+1)', 'Error'];
                datosExportar = currentData;
                break;
            case 'punto_fijo':
                columnas = ['Iteración', 'X_n', 'X_n+1', 'Error'];
                datosExportar = currentData;
                break;
        }
        
        // Crear libro de Excel
        const wb = XLSX.utils.book_new();
        const ws = XLSX.utils.aoa_to_sheet([
            [`Método: ${currentMethod}`],
            [`Función: ${currentFunction}`],
            [],
            columnas,
            ...datosExportar
        ]);
        
        XLSX.utils.book_append_sheet(wb, ws, 'Resultados');
        
        // Descargar
        XLSX.writeFile(wb, `resultados_${currentMethod}.xlsx`);
    });
    
    // Exportar a PDF
    exportarPdfBtn.addEventListener('click', function() {
        if (!currentData) {
            alert('No hay datos para exportar');
            return;
        }
        
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        
        // Título
        doc.setFontSize(18);
        doc.text(`Resultados - Método ${currentMethod}`, 105, 15, { align: 'center' });
        doc.setFontSize(12);
        doc.text(`Función: ${currentFunction}`, 14, 25);
        
        // Configurar columnas para la tabla
        let columnas = [];
        let datosTabla = [];
        
        switch(currentMethod) {
            case 'newton':
                columnas = ['Iteración', 'X_i-1', 'f(X_i-1)', "f'(X_i-1)", 'X_i', 'Error'];
                datosTabla = currentData.map(fila => [
                    fila.iter,
                    fila.x.toFixed(6),
                    fila.fx.toFixed(6),
                    fila.dfx.toFixed(6),
                    fila.x_next.toFixed(6),
                    fila.error.toFixed(6)
                ]);
                break;
            case 'secante':
                columnas = ['Iteración', 'X_i-1', 'X_i', 'f(X_i-1)', 'f(X_i)', 'X_i+1', 'f(X_i+1)', 'Error'];
                datosTabla = currentData.map(fila => [
                    fila[0],
                    fila[1].toFixed(6),
                    fila[2].toFixed(6),
                    fila[3].toFixed(6),
                    fila[4].toFixed(6),
                    fila[5].toFixed(6),
                    fila[6].toFixed(6),
                    fila[7].toFixed(6)
                ]);
                break;
            case 'punto_fijo':
                columnas = ['Iteración', 'X_n', 'X_n+1', 'Error'];
                datosTabla = currentData.map(fila => [
                    fila[0],
                    fila[1].toFixed(6),
                    fila[2].toFixed(6),
                    fila[3].toFixed(6)
                ]);
                break;
        }
        
        // Agregar tabla
        doc.autoTable({
            head: [columnas],
            body: datosTabla,
            startY: 30,
            styles: {
                fontSize: 8,
                cellPadding: 2,
                overflow: 'linebreak'
            },
            columnStyles: {
                0: { cellWidth: 20 },
                1: { cellWidth: 25 },
                2: { cellWidth: 25 },
                3: { cellWidth: 25 },
                4: { cellWidth: 25 },
                5: { cellWidth: 25 }
            }
        });
        
        // Descargar
        doc.save(`resultados_${currentMethod}.pdf`);
    });
});