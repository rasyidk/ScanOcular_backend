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
   - api/klinik/ [POST]
        Schema {
         "nama_klinik" : "klinik 1",
         "kode_pos" : "55513",
         "alamat" : "kalirase, trimulyo"
        }
        Res [201/404]{
         "message": "Klinik registered successfully",
         "id": 5,
         "nama_klinik": "klinik 1",
         "alamat": "kalirase, trimulyo",
         "kode_pos": "55513"
        }
        - api/klinik/{id} [GET]
        RES [200/404]{
        "id": 2,
        "name": "klinik 2"
        }

   - api/klink/{id} [DELETE]
        RES [200/404]{
           "message": "Klinik deleted successfully"
        }
   
       
       
