function HtmlConsole(element) {
    this._orginal_functions = {};
    this.element = element || document.body;
}
HtmlConsole.prototype._add_log = function(level) {
    var old_function = console[level];
    this._orginal_functions[level] = old_function;
    return function() {
        try {
            old_function.apply(null, arguments);
        } catch (e) {
            try {
                old_function(arguments);
            } catch (e) {}
        }
        var args = [].slice.call(arguments);
        var err = document.createElement('div');
        err.setAttribute('class', 'entry ' + level);
        if (args.length === 0) {
            // pass
        } else {
            if (typeof args[0] === 'string') {
                err.appendChild(document.createTextNode(args[0]));
                args.shift();
            }
            if (args.length === 1) {
                err.appendChild(prettyPrint(args[0]));
            } else if (args.length > 1) {
                err.appendChild(prettyPrint(args));
            }
        }
        this.element.appendChild(err);
        err.scrollIntoView({behavior: 'smooth', block: 'end'});
    }.bind(this);
};
HtmlConsole.prototype.register = function (onerror=true) {
    console.debug     = this._add_log('debug');
    console.log       = this._add_log('log');
    console.error     = this._add_log('error');
    console.exception = this._add_log('exception');
    console.info      = this._add_log('info');
    console.warn      = this._add_log('warn');
    if (onerror) {
        window.onerror = console.error;
    }
};
HtmlConsole.prototype.unregister = function () {
    console.debug     = this._orginal_functions['debug'];
    console.log       = this._orginal_functions['log'];
    console.error     = this._orginal_functions['error'];
    console.exception = this._orginal_functions['exception'];
    console.info      = this._orginal_functions['info'];
    console.warn      = this._orginal_functions['warn'];
};
HtmlConsole.prototype.test = function (message = 'test') {
    console.debug(message);
    console.log(message);
    console.info(message);
    console.warn(message);
    console.error(message);
    console.exception(message);
};
