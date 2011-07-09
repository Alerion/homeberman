jQuery.Game = jQuery.Game || {};

jQuery.Game.BasePlayer = jQuery.inherit(jQuery.util.Observable, {
    cell: null, //jQuery.Game.Cell
    isDead: false,
    name: '',
    isPlayer: false, //is this current player
    constructor : function(config){
        jQuery.extend(this, config);
        jQuery.Game.BasePlayer.superclass.constructor.call(this, config);
        this.init();
    },
    init: function(){
        this.cell.setPlayer(this);
    }
});

jQuery.Game.Player = jQuery.inherit(jQuery.Game.BasePlayer, {
    cell: null, //jQuery.Game.Cell
    isDead: false,
    isPlayer: true,
    init: function(){
        jQuery.Game.Player.superclass.init.call(this);
    }
});

jQuery.Game.Enemy = jQuery.inherit(jQuery.Game.BasePlayer, {
    cell: null, //jQuery.Game.Cell
    isDead: false,
    init: function(){
        jQuery.Game.Enemy.superclass.init.call(this);
    }
});