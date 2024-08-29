document.getElementById('file-upload').addEventListener('change', function() {
    const fileInput = this;
    const fileName = fileInput.files[0].name;
    const fileExtension = fileName.split('.').pop().toLowerCase();

    if (fileExtension !== 'pdf') {
        alert('Por favor, selecione um arquivo PDF.');
        fileInput.value = ''; // Limpa o campo de input
        document.getElementById('file-name').textContent = '';
    } else {
        document.getElementById('file-name').textContent = `Arquivo selecionado: ${fileName}`;
    }
});
