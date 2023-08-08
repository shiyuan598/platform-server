/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ 92:
/***/ ((module, __unused_webpack_exports, __nccwpck_require__) => {

const EventEmitter = __nccwpck_require__(361);
const path = __nccwpck_require__(17);
const { fork } = __nccwpck_require__(81);
const uuid = __nccwpck_require__(160);

const daemonPath = __nccwpck_require__.ab + "daemon.js";

class BackgroundScheduledTask extends EventEmitter {
    constructor(cronExpression, taskPath, options){
        super();
        if(!options){
            options = {
                scheduled: true,
                recoverMissedExecutions: false,
            };
        }
        this.cronExpression = cronExpression;
        this.taskPath = taskPath;
        this.options = options;
        this.options.name = this.options.name || uuid.v4();

        if(options.scheduled){
            this.start();
        }
    }

    start() {
        this.stop();
        this.forkProcess = fork(__nccwpck_require__.ab + "daemon.js");

        this.forkProcess.on('message', (message) => {
            switch(message.type){
            case 'task-done':
                this.emit('task-done', message.result);
                break;
            }
        });

        let options = this.options;
        options.scheduled = true;
        
        this.forkProcess.send({
            type: 'register',
            path: path.resolve(this.taskPath),
            cron: this.cronExpression,
            options: options
        });
    }
    
    stop(){
        if(this.forkProcess){
            this.forkProcess.kill();
        }
    }

    pid() {
        if(this.forkProcess){
            return this.forkProcess.pid;
        }
    }

    isRunning(){
        return !this.forkProcess.killed;
    }
}

module.exports = BackgroundScheduledTask;

/***/ }),

/***/ 896:
/***/ ((module) => {

"use strict";

module.exports = (() => {
    function convertAsterisk(expression, replecement){
        if(expression.indexOf('*') !== -1){
            return expression.replace('*', replecement);
        }
        return expression;
    }

    function convertAsterisksToRanges(expressions){
        expressions[0] = convertAsterisk(expressions[0], '0-59');
        expressions[1] = convertAsterisk(expressions[1], '0-59');
        expressions[2] = convertAsterisk(expressions[2], '0-23');
        expressions[3] = convertAsterisk(expressions[3], '1-31');
        expressions[4] = convertAsterisk(expressions[4], '1-12');
        expressions[5] = convertAsterisk(expressions[5], '0-6');
        return expressions;
    }

    return convertAsterisksToRanges;
})();


/***/ }),

/***/ 486:
/***/ ((module, __unused_webpack_exports, __nccwpck_require__) => {

"use strict";


const monthNamesConversion = __nccwpck_require__(442);
const weekDayNamesConversion = __nccwpck_require__(307);
const convertAsterisksToRanges = __nccwpck_require__(896);
const convertRanges = __nccwpck_require__(119);
const convertSteps = __nccwpck_require__(366);

module.exports = (() => {

    function appendSeccondExpression(expressions){
        if(expressions.length === 5){
            return ['0'].concat(expressions);
        }
        return expressions;
    }

    function removeSpaces(str) {
        return str.replace(/\s{2,}/g, ' ').trim();
    }

    // Function that takes care of normalization.
    function normalizeIntegers(expressions) {
        for (let i=0; i < expressions.length; i++){
            const numbers = expressions[i].split(',');
            for (let j=0; j<numbers.length; j++){
                numbers[j] = parseInt(numbers[j]);
            }
            expressions[i] = numbers;
        }
        return expressions;
    }

    /*
   * The node-cron core allows only numbers (including multiple numbers e.g 1,2).
   * This module is going to translate the month names, week day names and ranges
   * to integers relatives.
   *
   * Month names example:
   *  - expression 0 1 1 January,Sep *
   *  - Will be translated to 0 1 1 1,9 *
   *
   * Week day names example:
   *  - expression 0 1 1 2 Monday,Sat
   *  - Will be translated to 0 1 1 1,5 *
   *
   * Ranges example:
   *  - expression 1-5 * * * *
   *  - Will be translated to 1,2,3,4,5 * * * *
   */
    function interprete(expression){
        let expressions = removeSpaces(expression).split(' ');
        expressions = appendSeccondExpression(expressions);
        expressions[4] = monthNamesConversion(expressions[4]);
        expressions[5] = weekDayNamesConversion(expressions[5]);
        expressions = convertAsterisksToRanges(expressions);
        expressions = convertRanges(expressions);
        expressions = convertSteps(expressions);

        expressions = normalizeIntegers(expressions);

        return expressions.join(' ');
    }

    return interprete;
})();


/***/ }),

/***/ 442:
/***/ ((module) => {

"use strict";

module.exports = (() => {
    const months = ['january','february','march','april','may','june','july',
        'august','september','october','november','december'];
    const shortMonths = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug',
        'sep', 'oct', 'nov', 'dec'];

    function convertMonthName(expression, items){
        for(let i = 0; i < items.length; i++){
            expression = expression.replace(new RegExp(items[i], 'gi'), parseInt(i, 10) + 1);
        }
        return expression;
    }

    function interprete(monthExpression){
        monthExpression = convertMonthName(monthExpression, months);
        monthExpression = convertMonthName(monthExpression, shortMonths);
        return monthExpression;
    }

    return interprete;
})();


/***/ }),

/***/ 119:
/***/ ((module) => {

"use strict";

module.exports = ( () => {
    function replaceWithRange(expression, text, init, end) {

        const numbers = [];
        let last = parseInt(end);
        let first = parseInt(init);

        if(first > last){
            last = parseInt(init);
            first = parseInt(end);
        }

        for(let i = first; i <= last; i++) {
            numbers.push(i);
        }

        return expression.replace(new RegExp(text, 'i'), numbers.join());
    }

    function convertRange(expression){
        const rangeRegEx = /(\d+)-(\d+)/;
        let match = rangeRegEx.exec(expression);
        while(match !== null && match.length > 0){
            expression = replaceWithRange(expression, match[0], match[1], match[2]);
            match = rangeRegEx.exec(expression);
        }
        return expression;
    }

    function convertAllRanges(expressions){
        for(let i = 0; i < expressions.length; i++){
            expressions[i] = convertRange(expressions[i]);
        }
        return expressions;
    }

    return convertAllRanges;
})();


/***/ }),

/***/ 366:
/***/ ((module) => {

"use strict";


module.exports = (() => {
    function convertSteps(expressions){
        var stepValuePattern = /^(.+)\/(\w+)$/;
        for(var i = 0; i < expressions.length; i++){
            var match = stepValuePattern.exec(expressions[i]);
            var isStepValue = match !== null && match.length > 0;
            if(isStepValue){
                var baseDivider = match[2];
                if(isNaN(baseDivider)){
                    throw baseDivider + ' is not a valid step value';
                }
                var values = match[1].split(',');
                var stepValues = [];
                var divider = parseInt(baseDivider, 10);
                for(var j = 0; j <= values.length; j++){
                    var value = parseInt(values[j], 10);
                    if(value % divider === 0){
                        stepValues.push(value);
                    }
                }
                expressions[i] = stepValues.join(',');
            }
        }
        return expressions;
    }

    return convertSteps;
})();


/***/ }),

/***/ 307:
/***/ ((module) => {

"use strict";

module.exports = (() => {
    const weekDays = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday',
        'friday', 'saturday'];
    const shortWeekDays = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'];

    function convertWeekDayName(expression, items){
        for(let i = 0; i < items.length; i++){
            expression = expression.replace(new RegExp(items[i], 'gi'), parseInt(i, 10));
        }
        return expression;
    }
  
    function convertWeekDays(expression){
        expression = expression.replace('7', '0');
        expression = convertWeekDayName(expression, weekDays);
        return convertWeekDayName(expression, shortWeekDays);
    }

    return convertWeekDays;
})();


/***/ }),

/***/ 934:
/***/ ((module, __unused_webpack_exports, __nccwpck_require__) => {

"use strict";


const ScheduledTask = __nccwpck_require__(948);
const BackgroundScheduledTask = __nccwpck_require__(92);
const validation = __nccwpck_require__(844);
const storage = __nccwpck_require__(218);

/**
 * @typedef {Object} CronScheduleOptions
 * @prop {boolean} [scheduled] if a scheduled task is ready and running to be
 *  performed when the time matches the cron expression.
 * @prop {string} [timezone] the timezone to execute the task in.
 */

/**
 * Creates a new task to execute the given function when the cron
 *  expression ticks.
 *
 * @param {string} expression The cron expression.
 * @param {Function} func The task to be executed.
 * @param {CronScheduleOptions} [options] A set of options for the scheduled task.
 * @returns {ScheduledTask} The scheduled task.
 */
function schedule(expression, func, options) {
    const task = createTask(expression, func, options);

    storage.save(task);

    return task;
}

function createTask(expression, func, options) {
    if (typeof func === 'string')
        return new BackgroundScheduledTask(expression, func, options);

    return new ScheduledTask(expression, func, options);
}

/**
 * Check if a cron expression is valid.
 *
 * @param {string} expression The cron expression.
 * @returns {boolean} Whether the expression is valid or not.
 */
function validate(expression) {
    try {
        validation(expression);

        return true;
    } catch (_) {
        return false;
    }
}

/**
 * Gets the scheduled tasks.
 *
 * @returns {ScheduledTask[]} The scheduled tasks.
 */
function getTasks() {
    return storage.getTasks();
}

module.exports = { schedule, validate, getTasks };


/***/ }),

/***/ 844:
/***/ ((module, __unused_webpack_exports, __nccwpck_require__) => {

"use strict";


const convertExpression = __nccwpck_require__(486);

const validationRegex = /^(?:\d+|\*|\*\/\d+)$/;

/**
 * @param {string} expression The Cron-Job expression.
 * @param {number} min The minimum value.
 * @param {number} max The maximum value.
 * @returns {boolean}
 */
function isValidExpression(expression, min, max) {
    const options = expression.split(',');

    for (const option of options) {
        const optionAsInt = parseInt(option, 10);

        if (
            (!Number.isNaN(optionAsInt) &&
                (optionAsInt < min || optionAsInt > max)) ||
            !validationRegex.test(option)
        )
            return false;
    }

    return true;
}

/**
 * @param {string} expression The Cron-Job expression.
 * @returns {boolean}
 */
function isInvalidSecond(expression) {
    return !isValidExpression(expression, 0, 59);
}

/**
 * @param {string} expression The Cron-Job expression.
 * @returns {boolean}
 */
function isInvalidMinute(expression) {
    return !isValidExpression(expression, 0, 59);
}

/**
 * @param {string} expression The Cron-Job expression.
 * @returns {boolean}
 */
function isInvalidHour(expression) {
    return !isValidExpression(expression, 0, 23);
}

/**
 * @param {string} expression The Cron-Job expression.
 * @returns {boolean}
 */
function isInvalidDayOfMonth(expression) {
    return !isValidExpression(expression, 1, 31);
}

/**
 * @param {string} expression The Cron-Job expression.
 * @returns {boolean}
 */
function isInvalidMonth(expression) {
    return !isValidExpression(expression, 1, 12);
}

/**
 * @param {string} expression The Cron-Job expression.
 * @returns {boolean}
 */
function isInvalidWeekDay(expression) {
    return !isValidExpression(expression, 0, 7);
}

/**
 * @param {string[]} patterns The Cron-Job expression patterns.
 * @param {string[]} executablePatterns The executable Cron-Job expression
 * patterns.
 * @returns {void}
 */
function validateFields(patterns, executablePatterns) {
    if (isInvalidSecond(executablePatterns[0]))
        throw new Error(`${patterns[0]} is a invalid expression for second`);

    if (isInvalidMinute(executablePatterns[1]))
        throw new Error(`${patterns[1]} is a invalid expression for minute`);

    if (isInvalidHour(executablePatterns[2]))
        throw new Error(`${patterns[2]} is a invalid expression for hour`);

    if (isInvalidDayOfMonth(executablePatterns[3]))
        throw new Error(
            `${patterns[3]} is a invalid expression for day of month`
        );

    if (isInvalidMonth(executablePatterns[4]))
        throw new Error(`${patterns[4]} is a invalid expression for month`);

    if (isInvalidWeekDay(executablePatterns[5]))
        throw new Error(`${patterns[5]} is a invalid expression for week day`);
}

/**
 * Validates a Cron-Job expression pattern.
 *
 * @param {string} pattern The Cron-Job expression pattern.
 * @returns {void}
 */
function validate(pattern) {
    if (typeof pattern !== 'string')
        throw new TypeError('pattern must be a string!');

    const patterns = pattern.split(' ');
    const executablePatterns = convertExpression(pattern).split(' ');

    if (patterns.length === 5) patterns.unshift('0');

    validateFields(patterns, executablePatterns);
}

module.exports = validate;


/***/ }),

/***/ 948:
/***/ ((module, __unused_webpack_exports, __nccwpck_require__) => {

"use strict";


const EventEmitter = __nccwpck_require__(361);
const Task = __nccwpck_require__(593);
const Scheduler = __nccwpck_require__(705);
const uuid = __nccwpck_require__(160);

class ScheduledTask extends EventEmitter {
    constructor(cronExpression, func, options) {
        super();
        if(!options){
            options = {
                scheduled: true,
                recoverMissedExecutions: false
            };
        }
      
        this.options = options;
        this.options.name = this.options.name || uuid.v4();

        this._task = new Task(func);
        this._scheduler = new Scheduler(cronExpression, options.timezone, options.recoverMissedExecutions);

        this._scheduler.on('scheduled-time-matched', (now) => {
            this.now(now);
        });

        if(options.scheduled !== false){
            this._scheduler.start();
        }
        
        if(options.runOnInit === true){
            this.now('init');
        }
    }
    
    now(now = 'manual') {
        let result = this._task.execute(now);
        this.emit('task-done', result);
    }
    
    start() {
        this._scheduler.start();  
    }
    
    stop() {
        this._scheduler.stop();
    }
}

module.exports = ScheduledTask;


/***/ }),

/***/ 705:
/***/ ((module, __unused_webpack_exports, __nccwpck_require__) => {

"use strict";


const EventEmitter = __nccwpck_require__(361);
const TimeMatcher = __nccwpck_require__(530);

class Scheduler extends EventEmitter{
    constructor(pattern, timezone, autorecover){
        super();
        this.timeMatcher = new TimeMatcher(pattern, timezone);
        this.autorecover = autorecover;
    }

    start(){
        // clear timeout if exists
        this.stop();

        let lastCheck = process.hrtime();
        let lastExecution = this.timeMatcher.apply(new Date());

        const matchTime = () => {
            const delay = 1000;
            const elapsedTime = process.hrtime(lastCheck);
            const elapsedMs = (elapsedTime[0] * 1e9 + elapsedTime[1]) / 1e6;
            const missedExecutions = Math.floor(elapsedMs / 1000);
            
            for(let i = missedExecutions; i >= 0; i--){
                const date = new Date(new Date().getTime() - i * 1000);
                let date_tmp = this.timeMatcher.apply(date);
                if(lastExecution.getTime() < date_tmp.getTime() && (i === 0 || this.autorecover) && this.timeMatcher.match(date)){
                    this.emit('scheduled-time-matched', date_tmp);
                    date_tmp.setMilliseconds(0);
                    lastExecution = date_tmp;
                }
            }
            lastCheck = process.hrtime();
            this.timeout = setTimeout(matchTime, delay);
        };
        matchTime();
    }

    stop(){
        if(this.timeout){
            clearTimeout(this.timeout);
        }
        this.timeout = null;
    }
}

module.exports = Scheduler;


/***/ }),

/***/ 218:
/***/ ((module, __unused_webpack_exports, __nccwpck_require__) => {

module.exports = (() => {
    if(!global.scheduledTasks){
        global.scheduledTasks = new Map();
    }
    
    return {
        save: (task) => {
            if(!task.options){
                const uuid = __nccwpck_require__(160);
                task.options = {};
                task.options.name = uuid.v4();
            }
            global.scheduledTasks.set(task.options.name, task);
        },
        getTasks: () => {
            return global.scheduledTasks;
        }
    };
})();

/***/ }),

/***/ 593:
/***/ ((module, __unused_webpack_exports, __nccwpck_require__) => {

"use strict";


const EventEmitter = __nccwpck_require__(361);

class Task extends EventEmitter{
    constructor(execution){
        super();
        if(typeof execution !== 'function') {
            throw 'execution must be a function';
        }
        this._execution = execution;
    }

    execute(now) {
        let exec;
        try {
            exec = this._execution(now);
        } catch (error) {
            return this.emit('task-failed', error);
        }
        
        if (exec instanceof Promise) {
            return exec
                .then(() => this.emit('task-finished'))
                .catch((error) => this.emit('task-failed', error));
        } else {
            this.emit('task-finished');
            return exec;
        }
    }
}

module.exports = Task;



/***/ }),

/***/ 530:
/***/ ((module, __unused_webpack_exports, __nccwpck_require__) => {

const validatePattern = __nccwpck_require__(844);
const convertExpression = __nccwpck_require__(486);

function matchPattern(pattern, value){
    if( pattern.indexOf(',') !== -1 ){
        const patterns = pattern.split(',');
        return patterns.indexOf(value.toString()) !== -1;
    }
    return pattern === value.toString();
}

class TimeMatcher{
    constructor(pattern, timezone){
        validatePattern(pattern);
        this.pattern = convertExpression(pattern);
        this.timezone = timezone;
        this.expressions = this.pattern.split(' ');
    }

    match(date){
        date = this.apply(date);

        const runOnSecond = matchPattern(this.expressions[0], date.getSeconds());
        const runOnMinute = matchPattern(this.expressions[1], date.getMinutes());
        const runOnHour = matchPattern(this.expressions[2], date.getHours());
        const runOnDay = matchPattern(this.expressions[3], date.getDate());
        const runOnMonth = matchPattern(this.expressions[4], date.getMonth() + 1);
        const runOnWeekDay = matchPattern(this.expressions[5], date.getDay());

        return runOnSecond && runOnMinute && runOnHour && runOnDay && runOnMonth && runOnWeekDay;
    }

    apply(date){
        if(this.timezone){
            const dtf = new Intl.DateTimeFormat('en-US', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hourCycle: 'h23',
                fractionalSecondDigits: 3,
                timeZone: this.timezone
            });
            
            return new Date(dtf.format(date));
        }
        
        return date;
    }
}

module.exports = TimeMatcher;

/***/ }),

/***/ 160:
/***/ ((__unused_webpack_module, exports, __nccwpck_require__) => {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
Object.defineProperty(exports, "v1", ({
  enumerable: true,
  get: function () {
    return _v.default;
  }
}));
Object.defineProperty(exports, "v3", ({
  enumerable: true,
  get: function () {
    return _v2.default;
  }
}));
Object.defineProperty(exports, "v4", ({
  enumerable: true,
  get: function () {
    return _v3.default;
  }
}));
Object.defineProperty(exports, "v5", ({
  enumerable: true,
  get: function () {
    return _v4.default;
  }
}));
Object.defineProperty(exports, "NIL", ({
  enumerable: true,
  get: function () {
    return _nil.default;
  }
}));
Object.defineProperty(exports, "version", ({
  enumerable: true,
  get: function () {
    return _version.default;
  }
}));
Object.defineProperty(exports, "validate", ({
  enumerable: true,
  get: function () {
    return _validate.default;
  }
}));
Object.defineProperty(exports, "stringify", ({
  enumerable: true,
  get: function () {
    return _stringify.default;
  }
}));
Object.defineProperty(exports, "parse", ({
  enumerable: true,
  get: function () {
    return _parse.default;
  }
}));

var _v = _interopRequireDefault(__nccwpck_require__(300));

var _v2 = _interopRequireDefault(__nccwpck_require__(392));

var _v3 = _interopRequireDefault(__nccwpck_require__(103));

var _v4 = _interopRequireDefault(__nccwpck_require__(223));

var _nil = _interopRequireDefault(__nccwpck_require__(540));

var _version = _interopRequireDefault(__nccwpck_require__(799));

var _validate = _interopRequireDefault(__nccwpck_require__(623));

var _stringify = _interopRequireDefault(__nccwpck_require__(792));

var _parse = _interopRequireDefault(__nccwpck_require__(19));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/***/ }),

/***/ 354:
/***/ ((__unused_webpack_module, exports, __nccwpck_require__) => {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var _crypto = _interopRequireDefault(__nccwpck_require__(113));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function md5(bytes) {
  if (Array.isArray(bytes)) {
    bytes = Buffer.from(bytes);
  } else if (typeof bytes === 'string') {
    bytes = Buffer.from(bytes, 'utf8');
  }

  return _crypto.default.createHash('md5').update(bytes).digest();
}

var _default = md5;
exports["default"] = _default;

/***/ }),

/***/ 540:
/***/ ((__unused_webpack_module, exports) => {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;
var _default = '00000000-0000-0000-0000-000000000000';
exports["default"] = _default;

/***/ }),

/***/ 19:
/***/ ((__unused_webpack_module, exports, __nccwpck_require__) => {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var _validate = _interopRequireDefault(__nccwpck_require__(623));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function parse(uuid) {
  if (!(0, _validate.default)(uuid)) {
    throw TypeError('Invalid UUID');
  }

  let v;
  const arr = new Uint8Array(16); // Parse ########-....-....-....-............

  arr[0] = (v = parseInt(uuid.slice(0, 8), 16)) >>> 24;
  arr[1] = v >>> 16 & 0xff;
  arr[2] = v >>> 8 & 0xff;
  arr[3] = v & 0xff; // Parse ........-####-....-....-............

  arr[4] = (v = parseInt(uuid.slice(9, 13), 16)) >>> 8;
  arr[5] = v & 0xff; // Parse ........-....-####-....-............

  arr[6] = (v = parseInt(uuid.slice(14, 18), 16)) >>> 8;
  arr[7] = v & 0xff; // Parse ........-....-....-####-............

  arr[8] = (v = parseInt(uuid.slice(19, 23), 16)) >>> 8;
  arr[9] = v & 0xff; // Parse ........-....-....-....-############
  // (Use "/" to avoid 32-bit truncation when bit-shifting high-order bytes)

  arr[10] = (v = parseInt(uuid.slice(24, 36), 16)) / 0x10000000000 & 0xff;
  arr[11] = v / 0x100000000 & 0xff;
  arr[12] = v >>> 24 & 0xff;
  arr[13] = v >>> 16 & 0xff;
  arr[14] = v >>> 8 & 0xff;
  arr[15] = v & 0xff;
  return arr;
}

var _default = parse;
exports["default"] = _default;

/***/ }),

/***/ 100:
/***/ ((__unused_webpack_module, exports) => {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;
var _default = /^(?:[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}|00000000-0000-0000-0000-000000000000)$/i;
exports["default"] = _default;

/***/ }),

/***/ 882:
/***/ ((__unused_webpack_module, exports, __nccwpck_require__) => {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = rng;

var _crypto = _interopRequireDefault(__nccwpck_require__(113));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

const rnds8Pool = new Uint8Array(256); // # of random values to pre-allocate

let poolPtr = rnds8Pool.length;

function rng() {
  if (poolPtr > rnds8Pool.length - 16) {
    _crypto.default.randomFillSync(rnds8Pool);

    poolPtr = 0;
  }

  return rnds8Pool.slice(poolPtr, poolPtr += 16);
}

/***/ }),

/***/ 134:
/***/ ((__unused_webpack_module, exports, __nccwpck_require__) => {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var _crypto = _interopRequireDefault(__nccwpck_require__(113));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function sha1(bytes) {
  if (Array.isArray(bytes)) {
    bytes = Buffer.from(bytes);
  } else if (typeof bytes === 'string') {
    bytes = Buffer.from(bytes, 'utf8');
  }

  return _crypto.default.createHash('sha1').update(bytes).digest();
}

var _default = sha1;
exports["default"] = _default;

/***/ }),

/***/ 792:
/***/ ((__unused_webpack_module, exports, __nccwpck_require__) => {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var _validate = _interopRequireDefault(__nccwpck_require__(623));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
 * Convert array of 16 byte values to UUID string format of the form:
 * XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
 */
const byteToHex = [];

for (let i = 0; i < 256; ++i) {
  byteToHex.push((i + 0x100).toString(16).substr(1));
}

function stringify(arr, offset = 0) {
  // Note: Be careful editing this code!  It's been tuned for performance
  // and works in ways you may not expect. See https://github.com/uuidjs/uuid/pull/434
  const uuid = (byteToHex[arr[offset + 0]] + byteToHex[arr[offset + 1]] + byteToHex[arr[offset + 2]] + byteToHex[arr[offset + 3]] + '-' + byteToHex[arr[offset + 4]] + byteToHex[arr[offset + 5]] + '-' + byteToHex[arr[offset + 6]] + byteToHex[arr[offset + 7]] + '-' + byteToHex[arr[offset + 8]] + byteToHex[arr[offset + 9]] + '-' + byteToHex[arr[offset + 10]] + byteToHex[arr[offset + 11]] + byteToHex[arr[offset + 12]] + byteToHex[arr[offset + 13]] + byteToHex[arr[offset + 14]] + byteToHex[arr[offset + 15]]).toLowerCase(); // Consistency check for valid UUID.  If this throws, it's likely due to one
  // of the following:
  // - One or more input array values don't map to a hex octet (leading to
  // "undefined" in the uuid)
  // - Invalid input values for the RFC `version` or `variant` fields

  if (!(0, _validate.default)(uuid)) {
    throw TypeError('Stringified UUID is invalid');
  }

  return uuid;
}

var _default = stringify;
exports["default"] = _default;

/***/ }),

/***/ 300:
/***/ ((__unused_webpack_module, exports, __nccwpck_require__) => {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var _rng = _interopRequireDefault(__nccwpck_require__(882));

var _stringify = _interopRequireDefault(__nccwpck_require__(792));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

// **`v1()` - Generate time-based UUID**
//
// Inspired by https://github.com/LiosK/UUID.js
// and http://docs.python.org/library/uuid.html
let _nodeId;

let _clockseq; // Previous uuid creation time


let _lastMSecs = 0;
let _lastNSecs = 0; // See https://github.com/uuidjs/uuid for API details

function v1(options, buf, offset) {
  let i = buf && offset || 0;
  const b = buf || new Array(16);
  options = options || {};
  let node = options.node || _nodeId;
  let clockseq = options.clockseq !== undefined ? options.clockseq : _clockseq; // node and clockseq need to be initialized to random values if they're not
  // specified.  We do this lazily to minimize issues related to insufficient
  // system entropy.  See #189

  if (node == null || clockseq == null) {
    const seedBytes = options.random || (options.rng || _rng.default)();

    if (node == null) {
      // Per 4.5, create and 48-bit node id, (47 random bits + multicast bit = 1)
      node = _nodeId = [seedBytes[0] | 0x01, seedBytes[1], seedBytes[2], seedBytes[3], seedBytes[4], seedBytes[5]];
    }

    if (clockseq == null) {
      // Per 4.2.2, randomize (14 bit) clockseq
      clockseq = _clockseq = (seedBytes[6] << 8 | seedBytes[7]) & 0x3fff;
    }
  } // UUID timestamps are 100 nano-second units since the Gregorian epoch,
  // (1582-10-15 00:00).  JSNumbers aren't precise enough for this, so
  // time is handled internally as 'msecs' (integer milliseconds) and 'nsecs'
  // (100-nanoseconds offset from msecs) since unix epoch, 1970-01-01 00:00.


  let msecs = options.msecs !== undefined ? options.msecs : Date.now(); // Per 4.2.1.2, use count of uuid's generated during the current clock
  // cycle to simulate higher resolution clock

  let nsecs = options.nsecs !== undefined ? options.nsecs : _lastNSecs + 1; // Time since last uuid creation (in msecs)

  const dt = msecs - _lastMSecs + (nsecs - _lastNSecs) / 10000; // Per 4.2.1.2, Bump clockseq on clock regression

  if (dt < 0 && options.clockseq === undefined) {
    clockseq = clockseq + 1 & 0x3fff;
  } // Reset nsecs if clock regresses (new clockseq) or we've moved onto a new
  // time interval


  if ((dt < 0 || msecs > _lastMSecs) && options.nsecs === undefined) {
    nsecs = 0;
  } // Per 4.2.1.2 Throw error if too many uuids are requested


  if (nsecs >= 10000) {
    throw new Error("uuid.v1(): Can't create more than 10M uuids/sec");
  }

  _lastMSecs = msecs;
  _lastNSecs = nsecs;
  _clockseq = clockseq; // Per 4.1.4 - Convert from unix epoch to Gregorian epoch

  msecs += 12219292800000; // `time_low`

  const tl = ((msecs & 0xfffffff) * 10000 + nsecs) % 0x100000000;
  b[i++] = tl >>> 24 & 0xff;
  b[i++] = tl >>> 16 & 0xff;
  b[i++] = tl >>> 8 & 0xff;
  b[i++] = tl & 0xff; // `time_mid`

  const tmh = msecs / 0x100000000 * 10000 & 0xfffffff;
  b[i++] = tmh >>> 8 & 0xff;
  b[i++] = tmh & 0xff; // `time_high_and_version`

  b[i++] = tmh >>> 24 & 0xf | 0x10; // include version

  b[i++] = tmh >>> 16 & 0xff; // `clock_seq_hi_and_reserved` (Per 4.2.2 - include variant)

  b[i++] = clockseq >>> 8 | 0x80; // `clock_seq_low`

  b[i++] = clockseq & 0xff; // `node`

  for (let n = 0; n < 6; ++n) {
    b[i + n] = node[n];
  }

  return buf || (0, _stringify.default)(b);
}

var _default = v1;
exports["default"] = _default;

/***/ }),

/***/ 392:
/***/ ((__unused_webpack_module, exports, __nccwpck_require__) => {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var _v = _interopRequireDefault(__nccwpck_require__(995));

var _md = _interopRequireDefault(__nccwpck_require__(354));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

const v3 = (0, _v.default)('v3', 0x30, _md.default);
var _default = v3;
exports["default"] = _default;

/***/ }),

/***/ 995:
/***/ ((__unused_webpack_module, exports, __nccwpck_require__) => {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = _default;
exports.URL = exports.DNS = void 0;

var _stringify = _interopRequireDefault(__nccwpck_require__(792));

var _parse = _interopRequireDefault(__nccwpck_require__(19));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function stringToBytes(str) {
  str = unescape(encodeURIComponent(str)); // UTF8 escape

  const bytes = [];

  for (let i = 0; i < str.length; ++i) {
    bytes.push(str.charCodeAt(i));
  }

  return bytes;
}

const DNS = '6ba7b810-9dad-11d1-80b4-00c04fd430c8';
exports.DNS = DNS;
const URL = '6ba7b811-9dad-11d1-80b4-00c04fd430c8';
exports.URL = URL;

function _default(name, version, hashfunc) {
  function generateUUID(value, namespace, buf, offset) {
    if (typeof value === 'string') {
      value = stringToBytes(value);
    }

    if (typeof namespace === 'string') {
      namespace = (0, _parse.default)(namespace);
    }

    if (namespace.length !== 16) {
      throw TypeError('Namespace must be array-like (16 iterable integer values, 0-255)');
    } // Compute hash of namespace and value, Per 4.3
    // Future: Use spread syntax when supported on all platforms, e.g. `bytes =
    // hashfunc([...namespace, ... value])`


    let bytes = new Uint8Array(16 + value.length);
    bytes.set(namespace);
    bytes.set(value, namespace.length);
    bytes = hashfunc(bytes);
    bytes[6] = bytes[6] & 0x0f | version;
    bytes[8] = bytes[8] & 0x3f | 0x80;

    if (buf) {
      offset = offset || 0;

      for (let i = 0; i < 16; ++i) {
        buf[offset + i] = bytes[i];
      }

      return buf;
    }

    return (0, _stringify.default)(bytes);
  } // Function#name is not settable on some platforms (#270)


  try {
    generateUUID.name = name; // eslint-disable-next-line no-empty
  } catch (err) {} // For CommonJS default export support


  generateUUID.DNS = DNS;
  generateUUID.URL = URL;
  return generateUUID;
}

/***/ }),

/***/ 103:
/***/ ((__unused_webpack_module, exports, __nccwpck_require__) => {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var _rng = _interopRequireDefault(__nccwpck_require__(882));

var _stringify = _interopRequireDefault(__nccwpck_require__(792));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function v4(options, buf, offset) {
  options = options || {};

  const rnds = options.random || (options.rng || _rng.default)(); // Per 4.4, set bits for version and `clock_seq_hi_and_reserved`


  rnds[6] = rnds[6] & 0x0f | 0x40;
  rnds[8] = rnds[8] & 0x3f | 0x80; // Copy bytes to buffer, if provided

  if (buf) {
    offset = offset || 0;

    for (let i = 0; i < 16; ++i) {
      buf[offset + i] = rnds[i];
    }

    return buf;
  }

  return (0, _stringify.default)(rnds);
}

var _default = v4;
exports["default"] = _default;

/***/ }),

/***/ 223:
/***/ ((__unused_webpack_module, exports, __nccwpck_require__) => {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var _v = _interopRequireDefault(__nccwpck_require__(995));

var _sha = _interopRequireDefault(__nccwpck_require__(134));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

const v5 = (0, _v.default)('v5', 0x50, _sha.default);
var _default = v5;
exports["default"] = _default;

/***/ }),

/***/ 623:
/***/ ((__unused_webpack_module, exports, __nccwpck_require__) => {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var _regex = _interopRequireDefault(__nccwpck_require__(100));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function validate(uuid) {
  return typeof uuid === 'string' && _regex.default.test(uuid);
}

var _default = validate;
exports["default"] = _default;

/***/ }),

/***/ 799:
/***/ ((__unused_webpack_module, exports, __nccwpck_require__) => {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var _validate = _interopRequireDefault(__nccwpck_require__(623));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function version(uuid) {
  if (!(0, _validate.default)(uuid)) {
    throw TypeError('Invalid UUID');
  }

  return parseInt(uuid.substr(14, 1), 16);
}

var _default = version;
exports["default"] = _default;

/***/ }),

/***/ 81:
/***/ ((module) => {

"use strict";
module.exports = require("child_process");

/***/ }),

/***/ 113:
/***/ ((module) => {

"use strict";
module.exports = require("crypto");

/***/ }),

/***/ 361:
/***/ ((module) => {

"use strict";
module.exports = require("events");

/***/ }),

/***/ 17:
/***/ ((module) => {

"use strict";
module.exports = require("path");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __nccwpck_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		var threw = true;
/******/ 		try {
/******/ 			__webpack_modules__[moduleId](module, module.exports, __nccwpck_require__);
/******/ 			threw = false;
/******/ 		} finally {
/******/ 			if(threw) delete __webpack_module_cache__[moduleId];
/******/ 		}
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/compat */
/******/ 	
/******/ 	if (typeof __nccwpck_require__ !== 'undefined') __nccwpck_require__.ab = __dirname + "/";
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};
// This entry need to be wrapped in an IIFE because it need to be isolated against other modules in the chunk.
(() => {
const { exec } = __nccwpck_require__(81);
const cron = __nccwpck_require__(934);

const url = "https://weread.qq.com/web/reader/4b332350813ab7c27g013503kc20321001cc20ad4d76f5ae";

const openWeRead = (url) => {
    // 要执行的 Bash 命令
    const command = `xdg-open ${url}`;

    // 使用 exec 函数执行 Bash 命令
    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error("执行命令时出现错误:", error.message);

            return;
        }

        // 输出命令执行的结果
        console.log("命令执行结果:", stdout);
    });
};

const runTask = (fn, ...params) => {
    // 定义一个要执行的定时任务
    const task = cron.schedule(
        "15 6,8,10,12,18 * * *",
        () => {
            console.log("定时任务正在执行...", (new Date()).toString());
            fn(...params);
        },
        {
            scheduled: true, // 是否启用定时任务，默认为 true

            timezone: "Asia/Shanghai" // 指定时区，可以根据需要更改
        }
    );

    // 定时任务开始执行
    task.start();
    console.info("定时任务开始执行");
};
runTask(openWeRead, url);

})();

module.exports = __webpack_exports__;
/******/ })()
;