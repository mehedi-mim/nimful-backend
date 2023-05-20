from config import get_config
from utils.helpers.mail_helpers import encoding_token


def verification_mail(data, email):
    template = f"""
<!DOCTYPE html
    PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <!-- Use Internet Explorer 9 Standards mode -->
    <meta http-equiv="x-ua-compatible" content="IE=9">
    <!-- Open Sans font -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,200;400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <title>Stickler</title>
    <style type="text/css">
        body,
        div,
        table,
        tr,
        tbody,
        thead,
        td,
        th,
        h1,
        h2,
        h3,
        h4,
        h5,
        h6
    </style>
</head>
<body style="
width: 600px;
margin: 0 auto;
">
    <center style="
    font-family: montserrat;
    background-color: #f9f9f9;
    margin: 0 auto;
    padding: 10px 44px;
    height:calc(100vh - 23px)
    ">
        <!-- section start -->
            <section style="font-family: montserrat; margin-bottom: 30px; background-color: #fff; text-align: left; padding:20px 40px; border-radius: 4px; margin-top: 30px">
             <table style="width:100%;">
                <tr>
                    <td style="text-align: left">
                        <a href="#">
                            <img src="https://stickler-dev.s3.ap-southeast-1.amazonaws.com/Logo.png" alt="logo" style="width: 100px;">
                        </a>
                    </td>
                    <td style="text-align: right;">
                        <a href="{get_config().login_url}" style="font-weight: 600;text-decoration: none;color: #005AFF;font-family: montserrat;font-size: 14px;">
                            Login to stickler.live
                        </a>
                    </td>
                </tr>
             </table>
            <hr/>
            <div>
                <p style="text-align:center">
                    <a href="#">
                        <img src="https://stickler-dev.s3.ap-southeast-1.amazonaws.com/verify.png" alt="logo" style="width: 37%">
                    </a>
                </p>
                <p style="
                text-align: center;
                font-size: 20px;
                font-family: montserrat;
                font-weight: 700;
                padding-bottom: 28px;
                ">
                  Verify your e-mail to finish signing up to Stickler
                </p>
                <div style="font-family: montserrat;font-weight: 400;font-size: 12px; color: #000">
                    <p>Thank you for choosing Stickler.</p>
                    <p style="padding-top: 20px;">Please confirm that {email} is your email address by clicking on the button below.</p>
                    <p style="padding-top: 20px;"> If you did not register with Stickler, please ignore this email.</p>
                </div>
                <!-- button start -->
                <p style="text-align:center; margin:25px 0px;">
                    <a href="{get_config().signup_verification_url}/{encoding_token(data['id'])}" style="background-color:#005AFF;border-radius: 6px;text-decoration: none;color: white;padding: 7px 50px;">Verify</a>
                </p>
                <!-- button end -->
            </div>
            </section>
        <!-- section end -->
    </center>
</body>
        """
    return template
