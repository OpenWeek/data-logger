



var game404Keys = [];
document.onkeydown = function (e)
{
    game404Keys[e.keyCode] = 1;
    return false;
}

document.onkeyup = function (e)
{
    game404Keys[e.keyCode] = 0;
    return false;
}



class Game404 = {

    constructor()
    {
        this.player = {
            x : 10,
            y : 250,
            score : 0,
            rotation : 0
        };
        
        var canvasElement = document.querySelector("#myCanvas");
        this.ctx = canvasElement.getContext("2d");
        
    }
    
    
    start()
    {
        
    }
    
    frame()
    {
        
    }
    
    
    draw()
    {
        
    }
    
    drawPlayer()
    {
        this.ctx.beginPath();
        this.ctx.moveTo(100, 100);
        this.ctx.lineTo(100, 300);
        this.ctx.lineTo(300, 300);
        this.ctx.closePath();

        // the outline
        this.ctx.lineWidth = 10;
        this.ctx.strokeStyle = '#666666';
        this.ctx.stroke();

    }
    
    
    
}