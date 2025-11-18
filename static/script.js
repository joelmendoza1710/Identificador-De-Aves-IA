const uploadBtn = document.getElementById('uploadBtn');
const fileInput = document.getElementById('fileInput');
const resultadoDiv = document.getElementById('resultado');
const descripcionEl = document.getElementById('descripcion');
const loadingEl = document.getElementById('loading');

uploadBtn.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) {
        alert("Por favor selecciona una imagen primero.");
        return;
    }

    resultadoDiv.classList.add('hidden');
    loadingEl.classList.remove('hidden');

    const formData = new FormData();
    formData.append('image', file);

    try {
        const res = await fetch('/api/identificar', {
            method: 'POST',
            body: formData
        });

        const data = await res.json();
        loadingEl.classList.add('hidden');

        if (data.error) {
            alert("Error: " + data.error);
            console.error(data.detalle);
            return;
        }

        descripcionEl.textContent = data.descripcion;
        resultadoDiv.classList.remove('hidden');
    } catch (err) {
        loadingEl.classList.add('hidden');
        alert("Error de conexión con el servidor.");
    }
});
