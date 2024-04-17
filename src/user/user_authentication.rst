.. _user_authentication:

User authentication
======================

PanDA services support both x509 and OIDC JWT (Json Web Token) based
authentications. For the Rubin experiment, the OIDC JWT based authentidation
method is enabled. It uses the IAM service to generate and valid user
tokens.

In the PanDA system, the token is similar to an ID card or visa. Every time when
accessing a PanDA service (PanDA Http service), the token will be attached together
with the user data to be sent to the Http service. The Http service will verify
the token to get the user information and authorize users.

- **User Registration**. To access the IAM system, users need to be registered into
  the IAM system.

- **Token Generation**. When trying to access a PanDA system, PanDA client will try
  to find a valid token. If there is no token available, PanDA will try the function
  to generate a token. In this step, users will be redirected to approve/sign the token.
  When a token is generated, it means the user has got an ID card to access
  the PanDA service.

- **Access PanDA**. When using PanDA client or bps client to access the PanDA service,
  PanDA will ask the users to show the token (PanDA client automatically checks and attach
  the token). The PanDA service will authorize users based on information in the token.

- **PanDA IAM service**. The IAM service is used to sign the tokens. One PanDA system can
  support multiple IAM services to sign the tokens. The USDF PanDA can use the *DOMA PanDA IAM*
  or *USDF PanDA IAM* (not available yet) to sign the tokens. The IAM service is similar
  to an ID card issuer office. When using the *DOMA PanDA IAM* to generate tokens for
  the USDF PanDA, it only means that the token is signed by the *DOMA PanDA IAM*. It doesn't
  mean you are logining to the DOMA PanDA server.

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

Detailed instructions for approving the URL:

- Copy the URL from the command hints to a web browser (any web browser).
  Then following the steps in the web browser. The URL is different at different
  time. So everytime you need to copy the URL from the command hints.

- After approving the URL in a web browser, you can come back to your
  command terminal. Then type 'y' (and return) to let the command continue
  to get the token.

After approval, the PanDA client leaves a token in the user home folder
and its used for future submissions unless the timeout has expired.

**A valid token is required for all PanDA services. If there is no valid
token, the *IAM user authentication* step will be triggered.**

Check token status
------------------

You can check the token status with this command below: ::

    [wguan@wguan-nb ~]$ panda_auth status
    Filename:       /home/wguan/.token
    Valid starting: 2024-04-15 17:13:48
    Expires:        2024-04-22 17:13:48
    Name:           Wen Guan
    Email:          Wen.Guan@cern.ch
    Groups:         Rubin,EIC,Rubin/production,panda_dev
    Organization:   PanDA-DOMA

**For different users, the output can be different, for example different groups**.

Authorization between IAM and the labs
--------------------------------------

**This part is for admins or for users who want to understand some logics behind IAM.
You can ignore this part.**

**This part is about the communication between services.**

IAM service needs the labs to authorize the IAM to sign the tokens for users in a lab.
For example, if IAM wants to sign a token for a user in Rubin Dex (https://dex.slac.stanford.edu/auth),
the IAM service at first needs to register in Rubin Dex and get approvals (with security information).
Then the IAM can sign tokens for users in Rubin Dex.

The IAM service needs to sign tokens for users from different labs or institutes. Does it mean
that the IAM service needs to get approvals from all these labs or institutes? Here we use CILogon.
CILogon is a service that many labs or institutes have already approved for OIDC tokens. The PanDA
IAM just needs to get approvals from the CILogon. Then PanDA IAM will be able to sign tokens for
users in these labs or institutes.
