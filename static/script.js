const _science = document.getElementById('science')
const _art = document.getElementById('art')
const _entertainment = document.getElementById('entertainment')


_science.addEventListener('click', ()=>{
    _art.style.transition = '0.8s'
    _art.style.transform = 'translateY(500%)'
    _entertainment.style.transition = '0.8s'
    _entertainment.style.transform = 'translateY(500%)'
})

_art.addEventListener('click', ()=>{
    _science.style.transition = '0.8s'
    _science.style.transform = 'translateY(500%)'
    _entertainment.style.transition = '0.8s'
    _entertainment.style.transform = 'translateY(500%)'
    _art.style.transform = 'translateY(-120%)'
})

_entertainment.addEventListener('click', ()=>{
    _art.style.transition = '0.8s'
    _art.style.transform = 'translateY(500%)'
    _science.style.transition = '0.8s'
    _science.style.transform = 'translateY(500%)'
    _entertainment.style.transform = 'translateY(-220%)'
})