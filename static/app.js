

document.getElementById('btn-forward').addEventListener('click', () => {
    console.log('forward button pressed')
    fetch("/action/forward", {
        method: "POST",
    })
    console.log('forward command sent')                 
})

document.getElementById('btn-left').addEventListener('click', () => {
    console.log('left button pressed')
    fetch("/action/left", {
        method: "POST",
    })         
    console.log('left command sent')
})

document.getElementById('btn-stop').addEventListener('click', () => {
    console.log('stop button pressed')
    fetch("/action/stop", {
        method: "POST",
    })
    console.log('stop command sent')
})

document.getElementById('btn-right').addEventListener('click', () => {
    console.log('right button pressed')
    fetch("/action/right", {
        method: "POST",
    })  
    console.log('right command sent')
})

document.getElementById('btn-backward').addEventListener('click', () => {
    console.log('backward button pressed')
    fetch("/action/backward", { 
        method: "POST",
    })

    console.log('backward command sent')
})
