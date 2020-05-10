const error = {

    /** 前端字符串检验错误 **/

    /* 注册、修改个人信息 */
    emptyUsername: 'Please input your username',
    incorrectUsername: '16 characters or less, cannot include "@"',

    /* 注册、找回密码 */
    emptyEmail: 'Please input your email',
    incorrectEmail: 'Please input correct email',

    /* 登录 */
    emptyUsernameOrEmail: 'Please input your username or email',
    incorrectUsernameOrEmail: 'Please input correct username or email',

    /* 注册、登录、找回密码、修改密码 */
    emptyPassword: 'Please input your password',
    incorrectPassword: 'Letters / numbers / English punctuation, Length 8-32',

    /* 注册、找回密码 */
    emptyCheckPassword: 'Please input your password again',
    incorrectCheckPassword: 'The two entered passwords are inconsistent',

    /* 修改密码 */
    emptyOldPassword: 'Please input your old password',
    emptyNewPassword: 'Please input your new password',
    emptyCheckNewPassword: 'Please input your new password again',
    incorrectCheckNewPassword: 'The two entered new passwords are inconsistent',

    /* 注册，找回密码 */
    emptyCode: 'Please input your code',
    incorrectCode: 'Verification code is 4 digits',

    /* 创建记忆 */
    emptyTitle: 'Please input your title',
    emptyContent: 'Please input your content',
    tooManyPictures: 'Only one picture can be added to a memory',
    tooManyAudios: 'Only one audio can be added to a memory',
    wrongPicture: 'The uploaded file can only be in jpg / png / gif format!',
    wrongAudio: 'The uploaded file can only be in mp3 / wav format!',
    tooLargeAudio: 'The uploaded file cannot exceed 10M!',

    /** 后端请求响应错误（后端返回的错误以 r 开头，前端显示的错误以 m 开头） **/

    /* 注册 */
    rIncorrectCode: '验证码错误',
    mIncorrectCode: 'Your verification code is incorrect!',
    rUsernameExist: '当前用户名已被使用',
    mUsernameExist: 'This username has already been used!',
    rEmailExist: '当前邮箱已经被使用',
    mEmailExist: 'This mailbox has already been used!',

    /* 登录 */
    rInvalidCredentials: 'invalid_credentials',
    mIncorrectUsernameOrPassword: 'Your username or password is incorrect!',
    mIncorrectEmailOrPassword: 'Your email or password is incorrect!',

};


export default error
