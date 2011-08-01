jQuery.StompListener = jQuery.inherit(jQuery.util.Observable, {
    constructor: function(config){
        this.user_id = config.user_id;
        this.socket = config.socket;
        this.MAX_RETRIES = 3;
        this.debug = config.debug || false;
        jQuery.StompListener.superclass.constructor.apply(this, arguments);
        this._initConnect();
    },
    _initConnect: function(){
    	this.addEvents('disconnect');
        var socket = this.socket;
        var stomp = this;
        this.connect_retries = 0;
        this.connect = new STOMPClient();
        this.connect.onopen = function(){
        	stomp.debug && console.log('onopen');
        };
        this.connect.onclose = (function(c) {
        	stomp.debug && console.log('onclose', c);
            this.connect_retries += 1;
            if (this.connect_retries > this.MAX_RETRIES){
            	stomp.debug && console.log('MAX_RETRIES limit')
                stomp.fireEvent('disconnect');
                return;
            }
            stomp.connect.connect.defer(this.connect_retries*500, stomp.connect, ['localhost', socket]);
        }).createDelegate(this);
        this.connect.onerror = function(error) { console.log('Error ' + error);};
        this.connect.onerrorframe = function(frame) { console.log('Error frame ' + frame);};
        this.connect.onconnectedframe = this.initSubscribes.createDelegate(this);
        this.connect.onmessageframe = this.onMessageFrame.createDelegate(this);
        this.connect.connect('localhost', socket);
    },
    initSubscribes: function(){
        this.connect_retries = 0;
        this.addEvents('user');
        this.connect.subscribe('/user/'+this.user_id);
    },
    onMessageFrame: function(frame){
        var dest = frame.headers.destination;
        var path = dest.split('/')[1];
        var data = jQuery.JSON.decode(frame.body);
        this.fireEvent(path, data);
    }
});

jQuery.SocketListener = jQuery.inherit(jQuery.util.Observable, {
    constructor: function(config){
        jQuery.StompListener.superclass.constructor.apply(this, arguments);
        
        sosketConfig = config.socketConfig || {};
        this.socket = new io.Socket(window.location.hostname, sosketConfig);
        this.addEvents('user');
        this.socket.connect();
        
        var that = this;
        this.socket.addEvent('message', function() {
            that.onMessage.apply(that, arguments);
        });
    },
    onMessage: function(data){
        this.fireEvent('user', data);
    }
});