jQuery.Game = jQuery.Game || {};

jQuery.Game.Controller = jQuery.inherit(jQuery.util.Observable, {
    map: null, //jQuery.Game.Map
    player: null, //jQuery.Game.Player
    enemies: {},
    bombs: {},
    stomp: null, //jQuery.StompListener
    finish_url: '',
    constructor : function(config){
        jQuery.extend(this, config);
        jQuery.Game.Controller.superclass.constructor.call(this, config);
        this.init();
    },
    init: function(){
        GameApi.load_players(this.initPlayers, this);
        this.map.on('cellclick', this.onCellClick, this);
        var that = this;
        jQuery(document).keypress(function(event){return that.onKeyPress(event)});
        this.stomp.on('user', this.onServerEvent, this);
    },
    onServerEvent: function(msg){
        switch(msg.event){
            case 'finish':
            document.location = this.finish_url;
            break;
            
            case 'respown':
            if (this.player.id == msg.player_id){
                var player = this.player;
            }else{
                var player = this.enemies[msg.player_id];
            }
            var cell = this.map.getCell(msg.cell.id);
            player.isDead = false;
            player.setCell(cell);            
            break;
            
            case 'user_moved':
            var player = this.enemies[msg.player_id];
            var cell = this.map.getCell(msg.cell.id);
            player.setCell(cell);
            break;
            
            case 'bomb_put':
            var cell = this.map.getCell(msg.cell.id);
            this.map.addBomb(cell);
            break;
            
            case 'bomb_explosion':
            this.map.explodeBomb(msg.bomb_id);
            break;
            
            case 'kill':
            if (msg.player_id == this.player.id){
                this.player.kill();
            }else{
                this.enemies[msg.player_id].kill();
            }
            break;
        }
    },
    initPlayers: function(data){
        this.player = new jQuery.Game.Player({
            id: data.player.id,
            name: data.player.name,
            cell: this.map.getCell(data.player.x, data.player.y),
            isDead: data.player.is_dead
        });
        for (var i=0, len=data.enemies.length; i<len; i++){
            var e = data.enemies[i];
            this.enemies[e.id] = new jQuery.Game.Enemy({
                id: e.id,
                name: e.name,
                cell: this.map.getCell(e.x, e.y),
                isDead: e.is_dead
            });
        }
    },
    canMove: function(cell){
        var dx = Math.abs(cell.x-this.player.cell.x);
        var dy = Math.abs(cell.y-this.player.cell.y);
        return ( 
            cell.isMoveable() && 
            dx <= 1 && 
            dy <= 1 &&
            dx != dy
        )
    },
    onKeyPress: function(event){
        var handled = false;

        switch(event.which){
            case 113:
            this.createBomb();
            handled = true;
            break;
            
            case 119:
            this.move(0, -1);
            handled = true;
            break;
            
            case 115:
            this.move(0, 1);
            handled = true;
            break;
            
            case 97:
            this.move(-1, 0);
            handled = true;
            break;
            
            case 100:
            this.move(1, 0);
            handled = true;
            break;
            
            return ! handled;
        }
    },
    move: function(dx, dy){
        var cell = this.player.cell;
        var new_cell = this.map.getCell(cell.x+dx, cell.y+dy);
        if (new_cell){
            this.onCellClick(new_cell);
        }
    },
    createBomb: function(){
        if (this.player.isDead) return;
        
        GameApi.put_bomb(this.player.cell.x, this.player.cell.y, function(response){
            if ( ! response) return;
            
            this.map.addBomb(this.player.cell);    
        }, this);
    },
    onCellClick: function(cell, map){
        if ( ! this.player.isDead && this.canMove(cell)){
            GameApi.move(cell.x, cell.y, function(response){
                if (response){
                    this.player.setCell(cell);
                }
            }, this);
        }
    }
});