let slideshows = document.querySelector('.slideshows');
let slides = document.querySelector('.slides');
let slide = document.querySelectorAll('.slide');
let points = document.querySelectorAll('.point > span');
let next = document.querySelector('.next');
let prev = document.querySelector('.prev');
let num = 0
let timer = 3000
function classSwitcher(){
    slide.forEach( i => i.classList.remove('show'))
    points.forEach( i => i.classList.remove('active'))
    slide[num].classList.add('show')
    points[num].classList.add('active')
}
let func = () => {
    num = (num == slide.length - 1) ? 0 : num + 1,
    classSwitcher()
}
let func2 = () => {
    num = (num == 0) ? slide.length - 1 : num - 1,
    classSwitcher()
}
let startSlide = setInterval(
    func , timer
)
points.forEach((point , index) => {
    point.addEventListener('click' , e => {
        num = index
        classSwitcher()
    })
})
next.addEventListener('click' , e => {
    func()
})
prev.addEventListener('click' , e => {
    func2()
})
slides.addEventListener('mouseover' , e => {
    clearInterval(startSlide)
})
slides.addEventListener('mouseleave' , e => {
    startSlide = setInterval(func , timer)
})
