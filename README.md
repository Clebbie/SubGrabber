# SubGrabber
This project will attempt to create a keyboard shortcut to grab twich subscriber names, and paste them into selected text areas.

## Gets the access_token 
https://id.twitch.tv/oauth2/authorize?client_id=a0eq55k1fyehqztfwcr0bx6y9b8j5z&redirect_uri=http://localhost:5000/auth_success&response_type=token&scope=channel:read:subscriptions

# Documentation

## Route / (index)
Serves index.html

### HTML Variables
- access_token (string) - Twitch OAuth Bearer token
- user_id (string) - Twitch user ID
- is_valid(boolean) - Whether or not the token is currently valid (using id.twitch /validate)
- first_time (boolean) - Whether or not the first time user

## Route /auth_success
Serves auth_success.html which is only reached from id.twitch success redirect.

## Route /auth
Sets up internal use of Twitch OAuth token.

### Request Body
```
{
    access_token: <token>   // The Twitch OAuth access token for the user
}
```

### Response Codes
- 200 - Token is validated and SubGrabber is successfully configured
- 401 - Token is invalid or SubGrabber was not successfully configured