[apiInner.mustache](./apiInner.mustache) :: [Version 5.0.0](https://github.com/OpenAPITools/openapi-generator/blob/v5.0.0/modules/openapi-generator/src/main/resources/typescript-axios/apiInner.mustache) with fixes from version [6f5076e](https://github.com/OpenAPITools/openapi-generator/blob/d7d5e53f2bad69cdb3dffae35eef1f3f1090a22c/modules/openapi-generator/src/main/resources/typescript-axios/apiInner.mustache).

Added fix for invalid handling of explode: true in GET parameters.
https://github.com/OpenAPITools/openapi-generator/issues/10438#issuecomment-1134719275

[urls.mustache](./urls.mustache) :: generates urls.js files, which includes constants
in form of `<operation name> = "<operation URI>"`.