Users authentication
======================

PanDA services support both x509 and OIDC JWT (Json Web Token) based
authentications. For the Rubin experiment, the OIDC JWT based authentidation
method is enabled. It uses the IAM service to generate and valid user
tokens.

IAM user registration
----------------------

During the PanDA evaluation procedure we are using the Indigo-IAM
(https://github.com/indigo-iam/iam ) system to provide users
authentication. We set up a dedicated instance of this system available
here::

    https://panda-iam-doma.cern.ch/login

WIth this system a user can create a new PanDA user profile for
submission tasks to PanDA. The registration process is starting from the
link provided above. Once a registration is approved by the
administrator, the user can start submitting tasks. It is up to the user
which credential provider to use during registration. It could be an
institutional account or general purpose services like Google or Github.
The only requirement is that the administrator should know user email
used in registration to match a person with a newly created account
during approval.


IAM user authentication
-----------------------

The *IAM user authentication* step will be triggered when connecting
to a PanDA service without a valid token.

Here are the steps for *IAM user authentication*::

    INFO : Please go to https://panda-iam-doma.cern.ch/device?user_code=OXIIWM
    and sign in. Waiting until authentication is completed

    INFO : Ready to get ID token?

    [y/n]

A user should proceed with the provided URL, login into the IAM system
with identity provider used for registration in the
https://panda-iam-doma.cern.ch and after confirm the payload:

.. image:: /_images/PayloadApproveScreen.jpg
   :width: 6.5in
   :height: 4.04167in

Fig 2. Payload approve screen

After approval, the PanDA client leaves a token in the user home folder
and its used for future submissions unless the timeout has expired.

**A valid token is required for all PanDA services. If there is no valid
token, the *IAM user authentication* step will be triggered.**
