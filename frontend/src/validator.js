const validator = {
    /* 字符串格式检测 */

    /* 正则表达式 */
    regUsername: /^[^@]{1,16}$/,
    regEmail: /^[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?$/,
    regPassword: /^([a-z_A-Z0-9-.!@#$%\\^&*)(+={}\][/",'<>~·`?:;|]){8,32}$/,
    regCode: /^\d{4}$/,

    /* 注册、修改个人信息 */
    username: (rule, value, callback) => {
        const reg = validator.regUsername;
        if (!reg.test(value)) {
            callback(new Error());
        }
        callback();
    },

    /* 登录 */
    usernameOrEmail: (rule, value, callback) => {
        const regUsername = validator.regUsername;
        const regEmail = validator.regEmail;
        if (!regUsername.test(value) && !regEmail.test(value)) {
            callback(new Error());
        }
        callback();
    },

    /* 登录、修改密码 */
    password: (rule, value, callback) => {
        const reg = validator.regPassword;
        if (!reg.test(value)) {
            callback(new Error());
        }
        callback();
    },

    /* 注册、找回密码 */
    code: (rule, value, callback) => {
        const reg = validator.regCode;
        if (!reg.test(value)) {
            callback(new Error());
        }
        callback();
    },
};

export default validator
