# ScanOcular_backend

localhost:3000 :

1. User 
     - api/users/signup [POST]
       - Shema {
          "name" : "syd",
          "NIK" : "3404131805050001",
          "email": "johndoe@example1222.com",
          "password": "yourpassword1",
          "alamat" : "sleman",
          "tanggal_lahir" : "1990-1-2"
      
      }
     - Res [201/404]{
          "message": "User registered successfully",
          "user_id": 5,
          "name": "syd",
          "email": "johndoe@example1222.com"
     }

     - api/users/signin [POST]
       - Schema{
            "email": "johndoe@example1.com",
            "password": "yourpassword1"
        }
       - Res [200/404] {
         {
            "message": "Sign-in successful!"
        }
       }

       
       
