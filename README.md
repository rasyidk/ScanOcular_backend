# ScanOcular_backend

localhost:3000 :

1. User 
     - api/users/signup [POST]
       Shema {
          "name" : "syd",
          "NIK" : "3404131805050001",
          "email": "johndoe@example1222.com",
          "password": "yourpassword1",
          "alamat" : "sleman",
          "tanggal_lahir" : "1990-1-2"
      
      }
        Res [201/404]{
          "message": "User registered successfully",
          "user_id": 5,
          "name": "syd",
          "email": "johndoe@example1222.com"
     }

     - api/users/signin [POST]
            Schema{
            "email": "johndoe@example1.com",
            "password": "yourpassword1"
        }
            Res [200/404] {
         {
            "message": "Sign-in successful!"
        }
       }

2. Dokter
        - api/users/dokter/signup/ [POST]
        Schema {
              "NIK": "1234567890123467",
              "STR" : "aaaa",
              "name": "John Doe",
              "email": "johndoe@example12.com",
              "password": "yourpassword12",
              "alamat": "123 Main St"
          }
        Res [201/404] {
              "message": "User registered successfully",
              "user_id": 3,
              "name": "John Doe",
              "email": "johndoe@example112.com"
        }
   
        - api/users/dokter/signin/ [POST]
        Schema {
         "email": "johndoe@example1.com",
         "password": "yourpassword1"
        }
        Res [200/404] {
             "message": "Sign-in successful!"
        }

3. Klinik
        -  api/klinik/
       
       
