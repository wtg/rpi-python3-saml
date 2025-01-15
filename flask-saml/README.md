This folder is for flask and saml using the [python3-saml](https://github.com/SAML-Toolkits/python3-saml/) package. More information could be found in the Github repo above.

The /metadata directory is where the metadata for the service provider (SP) is located. It should be kept as a URL rather than a file.

The certifications that are generated should go under /saml/certs.

You should change settings.json and advanced_settings.json to where your application is.

The lastest python version and requirement.txt that we tested is in this project.

```
Project Structure:
├── README
├── app.py
├── requirements.txt
├── saml
│   ├── advanced_settings.json
│   ├── certs
│   │   ├── README
│   │   ├── sp.crt (you generate this)
│   │   └── sp.key (you generate this)
│   └── settings.json
└── templates
    ├── attrs.html
    ├── base.html
    └── index.html
```