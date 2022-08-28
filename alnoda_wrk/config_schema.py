{
    'name': {
        'required': True,
        'type': 'string',
    },
    'doc_url': 
    {
        'required': True,
        'type': 'string',
    },
    'author': 
    {
        'required': True,
        'type': 'string',
    },
    'version': 
    {
        'required': True,
    },
    'description': 
    {
        'required': True,
        'type': 'string',
    },
    'logo': 
    {
        'required': False,
        'type': 'string',
    },
    'favicon': 
    {
        'required': False,
        'type': 'string',
    },
    'styles': 
    {
        'required': False,
        'type': 'dict',
        'schema': 
        {
            'font': 
            {
                'required': False,
                'type': 'string',
            },
            'colors': 
            {
                'required': False,
                'type': 'dict',
                'keysrules': 
                {
                    'type': 'string',
                    'allowed': ['light', 'dark'],
                },
                'valuesrules': 
                {
                    'type': 'dict',
                    'schema': 
                    {
                        'primary': 
                        {
                            'required': False,
                            'type': 'string',
                        },
                        'accent': 
                        {
                            'required': False,
                            'type': 'string',
                        },
                        'background': 
                        {
                            'required': False,
                            'type': 'string',
                        },
                        'subtitle': 
                        {
                            'required': False,
                            'type': 'string',
                        },
                        'text': 
                        {
                            'required': False,
                            'type': 'string',
                        },
                        'title': 
                        {
                            'required': False,
                            'type': 'string',
                        },
                        'code': 
                        {
                            'required': False,
                            'type': 'string',
                        },
                    }
                },
            },
            'common_colors':
            {
                'required': False,
                'type': 'dict',
                'schema':
                {
                    'header': 
                    {
                        'required': False,
                        'type': 'string',
                    },
                    'nav': 
                    {
                        'required': False,
                        'type': 'string',
                    },
                }
            },
        },
    },
    'pages': 
    {
        'required': False,
        'type': 'dict',
        'keysrules': 
        {
            'type': 'string',
            'allowed': ['home', 'admin', 'my_apps'],
        },
        'valuesrules': 
        {
            'type': 'list',
            'schema': 
            {
                'type': 'dict',
                'schema': 
                {
                    'name': 
                    {
                        'required': True,
                        'type': 'string',
                    },
                    'port': 
                    {
                        'required': True,
                        'type': 'integer',
                        'min': 8020,
                        'max': 8040,
                    },
                    'path': 
                    {
                        'required': False,
                        'type': 'string',
                    },
                    'title': 
                    {
                        'required': True,
                        'type': 'string',
                    },
                    'description': 
                    {
                        'required': True,
                        'type': 'string',
                    },
                    'image': 
                    {
                        'required': True,
                        'type': 'string',
                    }
                }
            }
        },
    },
    'start': 
    {
        'required': False,
        'type': 'list',
        'schema': 
        {
            'type': 'dict',
            'schema': 
            {
                'name': 
                {
                    'required': True,
                    'type': 'string',
                },
                'cmd': 
                {
                    'required': True,
                    'type': 'string',
                },
                'folder': 
                {
                    'required': False,
                    'type': 'string',
                },
                'env_vars': 
                {
                    'required': False,
                    'type': 'list',
                    'schema':
                    {
                        'type': 'dict',
                        'schema': 
                        {
                            'name': 
                            {
                                'required': True,
                                'type': 'string',
                            },
                            'value': 
                            {
                                'required': True,
                                'type': 'string',
                            }
                        }
                    }
                },
            }
        }
    },
}