jQuery.Game = jQuery.Game || {};

jQuery.Game.EMPTY = 0;
jQuery.Game.WALL = 1;

jQuery.Game.Cell = jQuery.inherit(jQuery.util.Observable, {
    size: null,
    node: null,
    x: null,
    y: null,
    type: null,
    player: null, //jQuery.Game.BasePlayer
    bomb: null, //jQuery.Game.Bomb
    key: 'x_y',
    constructor : function(config){
        this.addEvents('click');
        jQuery.extend(this, config);
        jQuery.Game.Cell.superclass.constructor.call(this, config);
        this.init();
    },
    init: function(){
        this.key = this.x+'_'+this.y;
        this.node.css('width', this.size);
        this.node.css('height', this.size);
        this.node.css('top', this.y*this.size);
        this.node.css('left', this.x*this.size);
        this.node.css('font-size', this.size);
        this.draw();
        var that = this;
        this.node.click(function(){that.onClick()});
    },
    draw: function(){
        if (this.player){
            this.drawPlayer();
            return
        };
        if (this.bomb){
            this.drawBomb();
            return
        };
        switch(this.type){
            case jQuery.Game.WALL:
            this.drawWall();
            break;
            default:
            this.drawEmpty();
            break;            
        }        
    },
    onClick: function(){
        this.fireEvent('click', this)
    },
    setPlayer: function(player){
        this.player = player;
        this.draw();
    },
    setBomb: function(bomb){
        this.bomb = bomb;
        this.draw();
    },
    isMoveable: function(){
        return this.type != jQuery.Game.WALL;
    },
    drawEmpty: function(){
        this.node.html('');
    },
    drawWall: function(){
        this.node.html('☰');
    },
    drawBomb: function(){
        this.node.html('☢');
    },    
    drawPlayer: function(){
        if (this.player.isPlayer){
            this.node.html('♞');
        }else{
            this.node.html('♿');
        }
    }
});

jQuery.Game.Map = jQuery.inherit(jQuery.util.Observable, {
    node: null,
    width: null,
    height: null,
    cell_size: 25,
    cells: {},
    constructor : function(config){
        this.addEvents('cellclick');
        jQuery.extend(this, config);
        jQuery.Game.Map.superclass.constructor.call(this, config);
        this.init();
    },
    init: function(){
        GameApi.load_map(this.render, this);
    },
    render: function(info){
        this.width = info['width'];
        this.height = info['height'];
        for (var x=0; x<this.width; x++){
            for (var y=0; y<this.height; y++){
                var key = x+'_'+y;
                var cell = new jQuery.Game.Cell({
                    size: this.cell_size,
                    x: x,
                    y: y,
                    node: jQuery('<div class="cell"></div>'),
                    type: info.cells[key].type
                });
                cell.on('click', this.onCellClick, this);
                this.cells[key] = cell;
                this.node.append(cell.node);
            }            
        }
    },
    onCellClick: function(cell){
        this.fireEvent('cellclick', cell, this);
    },
    getCell: function(x, y){
        if (x && y){
            return this.cells[x+'_'+y];
        }
        return this.cells[x];
    }
});
