jQuery.Game = jQuery.Game || {};

jQuery.Game.Controller = jQuery.inherit(jQuery.util.Observable, {
    map: null, //jQuery.Game.Map
    player: null, //jQuery.Game.Player
    enemies: {},
    constructor : function(config){
        jQuery.extend(this, config);
        jQuery.Game.Controller.superclass.constructor.call(this, config);
        this.init();
    },
    init: function(){
        GameApi.load_players(this.initPlayers, this);
    },
    initPlayers: function(data){
        this.player = new jQuery.Game.Player({
            name: data.player.name,
            cell: this.map.getCell(data.player.x, data.player.y)
        });
        for (var i=0, len=data.enemies.length; i<len; i++){
            var e = data.enemies[i];
            this.enemies[e.id] = new jQuery.Game.Enemy({
                name: e.name,
                cell: this.map.getCell(e.x, e.y)
            });
        }
    }
});