jQuery.Game = jQuery.Game || {};

jQuery.Game.EMPTY = 0;
jQuery.Game.WALL = 1;

jQuery.Game.Cell = jQuery.inherit(jQuery.util.Observable, {
    size: null,
    node: null,
    x: null,
    y: null,
    type: null,
    bomb: null, //jQuery.Game.Bomb
    id: 'x_y',
    playersNum: 0,
    constructor : function(config){
        this.addEvents('click');
        jQuery.extend(this, config);
        jQuery.Game.Cell.superclass.constructor.call(this, config);
        this.init();
    },
    init: function(){
        this.players = {};
        this.node.css('width', this.size);
        this.node.css('height', this.size);
        this.node.css('top', this.y*this.size);
        this.node.css('left', this.x*this.size);
        this.node.css('font-size', this.size);
        this.draw();
        var that = this;
        this.node.click(function(){that.onClick()});
        
        this.dellayedDraw = new jQuery.util.DelayedTask(this.draw, this);
    },
    draw: function(){
        if (this.playersNum){
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
        if ( ! this.players[player.id]){
            this.playersNum ++;
            this.players[player.id] = player;
            this.draw();            
        }
    },
    removePlayer: function(player){
        if (this.players[player.id]){
            this.playersNum--;
            delete this.players[player.id];
            this.draw();         
        }        
    },
    setBomb: function(bomb){
        this.bomb = bomb;
        this.draw();
    },
    setExplosion: function(){
        this.bomb = null;
        this.drawExplosion();
    },
    isMoveable: function(){
        return this.type != jQuery.Game.WALL;
    },
    drawEmpty: function(){
        this.node.html('');
        this.node.attr('class', 'cell empty');
    },
    drawWall: function(){
        this.node.html('');
        this.node.attr('class', 'cell wall');
    },
    drawBomb: function(){
        this.node.html('');
        this.node.attr('class', 'cell bomb');
    },    
    drawPlayer: function(){
        for (key in this.players){
            if (this.players[key].isPlayer && ! this.players[key].isDead){
                //this.node.html('♞');
                this.node.attr('class', 'cell player');
                return
            }
        }
        
        for (key in this.players){
            if ( ! this.players[key].isDead){
                //this.node.html('♿');
                this.node.attr('class', 'cell enemy');
                return
            }
        }
        this.node.html('☦');
        this.node.attr('class', 'cell grave');
    },
    drawExplosion: function(){
        if (this.isMoveable()){
            //this.node.html('☠');
            this.node.attr('class', 'cell explosion');
            this.dellayedDraw.delay(700);            
        }
    }
});

jQuery.Game.Map = jQuery.inherit(jQuery.util.Observable, {
    node: null,
    width: null,
    height: null,
    cell_size: 25,
    cells: {},
    bombs: {},
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
                var cell_info = info.cells[key];
                
                var config = {
                    size: this.cell_size,
                    node: jQuery('<div class="cell"></div>')
                };
                jQuery.extend(config, cell_info);
                
                var cell = new jQuery.Game.Cell(config);
                cell.on('click', this.onCellClick, this);
                this.cells[cell.id] = cell;
                if (cell_info.has_bomb){
                    this.addBomb(cell);
                }
                this.node.append(cell.node);
            }            
        }
        this.node.css('width', this.width*this.cell_size);
        this.node.css('height', this.height*this.cell_size);
    },
    onCellClick: function(cell){
        this.fireEvent('cellclick', cell, this);
    },
    getCell: function(x, y){
        if (typeof x != 'undefined' && typeof y != 'undefined'){
            return this.cells[x+'_'+y];
        }
        return this.cells[x];
    },
    addBomb: function(cell){
        var bomb = new jQuery.Game.Bomb({
            cell: cell
        });
        this.bombs[bomb.id] = bomb;          
    },
    explodeBomb: function(bomb_id){
        var bomb = this.bombs[bomb_id];
        if (bomb){
            bomb.explode();
            delete this.bombs[bomb_id];
        }
    }
});

jQuery.Game.Bomb = jQuery.inherit(jQuery.util.Observable, {
    cell: null, //jQuery.Game.Cell
    constructor : function(config){
        jQuery.extend(this, config);
        jQuery.Game.Bomb.superclass.constructor.call(this, config);
        this.init();
        this.id = this.cell.id;
    },
    init: function(){
        this.cell.setBomb(this);
    },
    explode: function(){
        this.cell.setExplosion();
    }
});