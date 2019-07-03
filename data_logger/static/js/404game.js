



var game404Keys = [];
document.onkeydown = function (e)
{
    game404Keys[e.keyCode] = 1;
    //return false;
}

document.onkeyup = function (e)
{
    game404Keys[e.keyCode] = 0;
    //return false;
}


window.onload = function()
{
    var g = new Game404();
}


class Game404 {

    constructor()
    {
        
        
        this.canvasElement = document.querySelector("#canvasGame");
        this.ctx = this.canvasElement.getContext("2d");
        this.w = this.canvasElement.offsetWidth;
        this.h = this.canvasElement.offsetHeight;
        this.ctx.canvas.width = this.w;
        this.ctx.canvas.height = this.h;
        
        this.player = {
            x : Math.random()*this.w,
            y : Math.random()*this.h,
            score : 0,
            rotation : 0,
            speedX : 0,
            speedY : 0
        };
           
        this.ennemies = [];
        
        
        //this.frame = this.frame.bind(this);
        setInterval(() => this.frame(),16);
    }
    
    
    frame()
    {
        if(game404Keys[39])this.player.rotation+=0.06;
        if(game404Keys[37])this.player.rotation-=0.06;
        if(game404Keys[38])
        {
            this.player.speedX -= Math.sin(this.player.rotation);
            this.player.speedY += Math.cos(this.player.rotation);
        }
        
        this.player.speedX /=1.1;
        this.player.speedY /=1.1;
        
        
        
        if(this.player.x<0)this.player.speedX = Math.abs(this.player.speedX );
        if(this.player.x>this.w)this.player.speedX = - Math.abs(this.player.speedX );
        if(this.player.y>this.h)this.player.speedY = - Math.abs(this.player.speedX );
        if(this.player.y<0)this.player.speedY =  Math.abs(this.player.speedX );
        
        
        this.player.x +=this.player.speedX;
        this.player.y +=this.player.speedY;
        
    //    this.ctx.clearRect(0, 0, this.w, this.h);
        this.drawPlayer();
        this.drawEnnemies();
    }
    
    
    drawEnnemies()
    {
        for(var i = 0;i<this.ennemies.length;i++)
        {
            var e = this.ennemies[i];
            this.ctx.beginPath();
            this.ctx.arc(e.x, e.y, 50, 0, 2 * Math.PI);
            this.ctx.closePath();
    
            // the outline
            this.ctx.lineWidth = 2;
            this.ctx.strokeStyle = 'black';
            this.ctx.stroke();
        }
    }
    
    drawPlayer()
    {
        
        this.ctx.save();
        this.ctx.translate(this.player.x,this.player.y);
        this.ctx.rotate(this.player.rotation);
        this.ctx.beginPath();
        this.ctx.moveTo(0,20);
        this.ctx.lineTo(-10, -10);
        this.ctx.lineTo(10, -10);
        this.ctx.closePath();

        // the outline
        this.ctx.lineWidth = 2;
        var p = this.player;
        var speed = p.speedX*p.speedX+p.speedY*p.speedY;
        var color = "rgb(0,"+Math.abs(p.speedX)*25+","+Math.abs(p.speedY)*25+")";
        this.ctx.strokeStyle = color;
        
        this.ctx.stroke();
        this.ctx.restore();

    }
    
    
    
}