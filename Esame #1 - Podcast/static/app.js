'use strict'

// FILTRA PODCAST PER CATEGORIA
document.querySelectorAll('#sezioneDrop > ul >li > a').forEach(link => {
    link.addEventListener('click', e => {
        e.preventDefault();

        const filter = e.target.dataset.tag;
        const podcasts = document.querySelectorAll('#pod_cast');

        for (let podcast of podcasts) {
            if (filter !== 'Tutti' && filter !== podcast.querySelector('#cat').innerText)
                podcast.classList.add('hide');
            else
                podcast.classList.remove('hide');
        }
    });
});

/* Le funzioni getInputValue() e getInputVal() servono per ottenere la parola che è stata
    scritta nella barra di ricerca dall'utente */

// CERCA UN EPISODIO USANDO IL TITOLO
function getInputValue(){
    var inputVal = document.getElementById("myInput").value;
    console.log(inputVal);
    const episodi = document.querySelectorAll('#epis');
    for (let episodio of episodi) {
        console.log(episodio.querySelector('#titoloEp').innerText)
        /* Con il metodo includes() possiamo verificare se la parola inserita dall'utente
        è presente in uno dei titoli degli episodi */
        if (!episodio.querySelector('#titoloEp').innerText.includes(inputVal))
            episodio.classList.add('hide');
        else 
            episodio.classList.remove('hide');

    }

}


// CERCA UN EPISODIO USANDO LA DESCRIZIONE
function getInputVal(){
    var inputVal = document.getElementById("myInput2").value;
    console.log(inputVal);

    const episodi = document.querySelectorAll('#epis');
    for (let episodio of episodi) {
        console.log(episodio.querySelector('#descr').innerText.includes(inputVal));
        /* Qui il metodo includes() è usato per verificare se ciò che è stato scritto dall'utente
        nella barra di ricerca è presente nella descrizione degli espidoi */
        if (!episodio.querySelector('#descr').innerText.includes(inputVal))
            episodio.classList.add('hide');
        else 
            episodio.classList.remove('hide');

    }
}
