import io
import json
from django.http import JsonResponse
import numpy as np
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from api.emails import send_otp_via_email
from .serializers import CustomUserSerializer, LoginSerializer, NoteSerializer, VerifyAccountSerializer
from .models import CustomUser, Note, UserImage
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from django.shortcuts import render
import cv2
from cvzone.PoseModule import PoseDetector

import os
import cvzone
from cvzone import *



@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of notes'
        },
        {
            'Endpoint': '/notes/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single note object'
        },
        {
            'Endpoint': '/notes/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new note with data sent in post request'
        },
        {
            'Endpoint': 'frontend/',
            'method': 'POST',
            'body': {'image': ""},
            'description': 'Creates new note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Delete and existing note'
        },
        {
            'Endpoint': '/Image/',
            'method': 'POST',
            'body': {'image': ""},
            'description': 'Delete and existing note'
        },
    ]
    return Response(routes)


@api_view(['GET'])
def getNotes(request):
    notes = Note.objects.all()
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getNote(request, pk):
    note = Note.objects.get(id=pk)
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def createNote(request):
    data = request.data

    note = Note.objects.create(
        body = data['body']
    )
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def createNote(request):
    data = request.data

    note = Note.objects.create(
        body = data['image']
    )
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)



@api_view(['PUT'])
def updateNote(request, pk):
    data = request.data

    note = Note.objects.get(id=pk)
    serializer = NoteSerializer(note, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def deleteNote(request, pk):
    note = Note.objects.get(id=pk)
    note.delete()
    return Response('Note was deleted!')


# class UploadImageView(APIView):
#     parser_classes = [MultiPartParser]

#     def post(self, request, format=None):
#         try:
#             image_file = request.FILES.get('image')
#             print(image_file)
            
            
#             img_data = image_file.read()
#             nparr = np.fromstring(img_data, np.uint8)
#             img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
#             detector = PoseDetector()
#             shirtFolderPath = "mediafiles/Image/1.png"
#             print(shirtFolderPath)
            

#             fixesRatio = 280 / 190  # widthOfShirt / widthOfPoint11to12
#             shirtRatioHeightWidth = 581 / 440

#             img = detector.findPose(img, draw=False)

#             while True:
#                 lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
#                 if lmList:
#                     lm11 = lmList[11][1:3]
#                     lm12 = lmList[12][1:3]
#                     imgShirt = cv2.imread(os.path.join(shirtFolderPath), cv2.IMREAD_UNCHANGED)

#                     widthOfShirt = int((lm11[0] - lm12[0]) * fixesRatio)
#                     imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)))
#                     currentScale = (lm11[0] - lm12[0]) / 190
#                     offset = int(44 * currentScale), int(48 * currentScale)

#                     try:
#                         img = overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
#                         print(img)
#                     except:
#                         pass
#                         my_model = UserImage.objects.create(image=img)
#                         print(my_model)
                
#                 return Response({'message': 'Image uploaded successfully'})
#         except Exception as e:
#             print(e)
#             return Response({'message': 'Error'})


# class UploadImageView(APIView):
#     parser_classes = [MultiPartParser]

#     def post(self, request, format=None):
#         try:
#             image_file = request.FILES.get('image')
#             print(image_file)

#             img_data = image_file.read()
#             nparr = np.fromstring(img_data, np.uint8)
#             img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#             detector = PoseDetector()
#             shirtFolderPath = "mediafiles/Image/1.png"
            

#             fixesRatio = 280 / 190  # widthOfShirt / widthOfPoint11to12
#             shirtRatioHeightWidth = 581 / 440

#             img = detector.findPose(img, draw=False)

#             lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
#             if lmList:
#                 lm11 = lmList[11][1:3]
#                 lm12 = lmList[12][1:3]
#                 imgShirt = cv2.imread(os.path.join(shirtFolderPath), cv2.IMREAD_UNCHANGED)

#                 widthOfShirt = int((lm11[0] - lm12[0]) * fixesRatio)
#                 imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)))
#                 currentScale = (lm11[0] - lm12[0]) / 190
#                 offset = int(44 * currentScale), int(48 * currentScale)

#                 try:
#                     img = overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
#                 except:
#                     pass

#             # Create UserImage instance with image file attached
#             my_model = UserImage.objects.create(image=image_file)

#             # Encode image as a JPEG or PNG in memory
#             _, img_encoded = cv2.imencode('.jpg', img)  # or '.png'

#             # Convert encoded image to bytes object
#             img_bytes = img_encoded.tobytes()

#             # Save image bytes to UserImage model instance
#             my_model.image.save('image.jpg', io.BytesIO(img_bytes), save=False)
#             my_model.save()

#             return Response({'message': 'Image uploaded successfully'})
#         except Exception as e:
#             print(e)
#             return Response({'message': 'Error'})

#*
# class UploadImageView(APIView):
#     parser_classes = [MultiPartParser]

#     def post(self, request, format=None):
#         """to get image from frontend and over"""
#         try:
#             image_file = request.FILES.get('image')
#             print(image_file)

#             img_data = image_file.read()
#             nparr = np.fromstring(img_data, np.uint8)
#             img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#             detector = PoseDetector()
#             shirtFolderPath = f"mediafiles/Image/{request.data.get('iName')}"
            

#             fixesRatio = 280 / 190  # widthOfShirt / widthOfPoint11to12
#             shirtRatioHeightWidth = 581 / 440

#             img = detector.findPose(img, draw=False)

#             lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
#             if lmList:
#                 lm11 = lmList[11][1:3]
#                 lm12 = lmList[12][1:3]
#                 imgShirt = cv2.imread(os.path.join(shirtFolderPath), cv2.IMREAD_UNCHANGED)
#                 m=int(lm11[0]-lm12[0])
#                 print("m id",m)
#                 widthOfShirt = int((lm11[0] - lm12[0]) * fixesRatio)
#                 print("widthOfShirt is ",widthOfShirt)
#                 imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)))
#                 currentScale = (lm11[0] - lm12[0]) / 190
#                 print("currentScale is",currentScale)
#                 offset = int(50 * currentScale), int(48 * currentScale)
#                 print("Offset is ",offset)

#                 try:
#                     img = overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
#                 except:
#                     pass


#             # Encode image as a JPEG or PNG in memory
#             _, img_encoded = cv2.imencode('.jpg', img)  # or '.png'

#             # Convert encoded image to bytes object
#             img_bytes = img_encoded.tobytes()
#             my_model = UserImage.objects.create(image= image_file)
#             x = image_file.name.split(".")
            
#             my_model.image.save(x[0] + "1."+x[-1], io.BytesIO(img_bytes), save=False)
#             my_model.save()
            
#             # Create UserImage instance with image file attached
            
            
#             # Save image bytes to UserImage model instance
            

#             return Response({'message': 'Image uploaded successfully'})
#         except Exception as e:
#             print(e)
#             return Response({'message': 'Error'})
#*

class UploadImageView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        """to get image from frontend and over"""
        try:
            image_file = request.FILES.get('image')
            print(image_file)

            img_data = image_file.read()
            nparr = np.fromstring(img_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            detector = PoseDetector()
            shirtFolderPath = f"mediafiles/Image/{request.data.get('iName')}"
            

            img = detector.findPose(img, draw=False)

            lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
            if lmList:
                lm11 = lmList[11][1:3]
                lm12 = lmList[12][1:3]
                imgShirt = cv2.imread(os.path.join(shirtFolderPath), cv2.IMREAD_UNCHANGED)

                (h,w,_) = imgShirt.shape
                print(h)
                print(w)
                shirtRatioHeightWidth = h / w  #ShirtHeight/ShirtWidth
                # print(shirtRatioHeightWidth)
                diff = int(lm11[0] - lm12[0])
                print(diff)
                fixesRatio = (diff + int(diff/2))/ diff  # widthOfShirt / widthOfPoint11to12
                print(fixesRatio)
                widthOfShirt = int((lm11[0]-lm12[0]) * fixesRatio)
                print(widthOfShirt)
                imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)))
                
                currentScale = (lm11[0] - lm12[0]) / diff
                print("currentScale is: ",currentScale)
                # offset = int(58.8 * currentScale), int(12 * currentScale)
                offset = int((diff/3.5) * currentScale), int((diff/4) * currentScale) 
                print("offset is : ",offset)

                try:
                    img = overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
                except:
                    pass


            # Encode image as a JPEG or PNG in memory
            _, img_encoded = cv2.imencode('.jpg', img)  # or '.png'

            # Convert encoded image to bytes object
            img_bytes = img_encoded.tobytes()
            my_model = UserImage.objects.create(image= image_file)
            x = image_file.name.split(".")
            
            my_model.image.save(x[0] + "1."+x[-1], io.BytesIO(img_bytes), save=False)
            my_model.save()
            
            # Create UserImage instance with image file attached
            
            
            # Save image bytes to UserImage model instance
            

            return Response({'message': 'Image uploaded successfully'})
        except Exception as e:
            print(e)
            return Response({'message': 'Error'})

# class UploadImageView(APIView):
#     parser_classes = [MultiPartParser]

#     def post(self, request, format=None):
#         """to get image from frontend and over"""
#         try:
#             image_file = request.FILES.get('image')
#             print(image_file)

#             img_data = image_file.read()
#             nparr = np.fromstring(img_data, np.uint8)
#             img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#             detector = PoseDetector()
#             img = detector.findPose(img, draw=False)
#             lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
#             lm11 = lmList[11][1:3]
#             lm12 = lmList[12][1:3]
#             lm23 = lmList[23][1:3]
#             lm24 = lmList[24][1:3]

            
#             shirtFolderPath = f"mediafiles/Image/{request.data.get('iName')}"
#             imgShirt = cv2.imread(os.path.join(shirtFolderPath), cv2.IMREAD_UNCHANGED)
#             detector = PoseDetector()
#             imgShirt = detector.findPose(imgShirt, draw=False)
#             lmsList, bboxInfo = detector.findPosition(imgShirt, bboxWithHands=False, draw=False)
#             lms11 = lmsList[11][1:3]
#             lms12 = lmsList[12][1:3]
#             lms23 = lmsList[23][1:3]
#             lms24 = lmsList[24][1:3]

#             shirtRatioHeightWidth = 581 / 440
            
#             wshirt1 = int(lms11[0] - lms12[0])
#             wshirt2 = int(lms23[0] - lms24[0])

#             #resize
#             imgShirt = cv2.resize(imgShirt,(190,shirtRatioHeightWidth))
#             wshirt2 = cv2.resize(wshirt2,(140,shirtRatioHeightWidth))

#             try:
#                     img = overlayPNG(img, imgShirt, (lm12[0], lm12[1]))
#             except:
#                     pass
            
#             # Encode image as a JPEG or PNG in memory
#             _, img_encoded = cv2.imencode('.jpg', img)  # or '.png'

#             # Convert encoded image to bytes object
#             img_bytes = img_encoded.tobytes()
#             my_model = UserImage.objects.create(image= image_file)
#             x = image_file.name.split(".")
            
#             my_model.image.save(x[0] + "1."+x[-1], io.BytesIO(img_bytes), save=False)
#             my_model.save()
            
#             # Create UserImage instance with image file attached
            
            
#             # Save image bytes to UserImage model instance
            

#             return Response({'message': 'Image uploaded successfully'})
#         except Exception as e:
#             print(e)
#             return Response({'message': 'Error'})



# class UploadImageView(APIView):
#     parser_classes = [MultiPartParser]

#     def post(self, request, format=None):
#         """to get image from frontend and over"""
#         try:
#             image_file = request.FILES.get('image')
#             print(image_file)

#             img_data = image_file.read()
#             nparr = np.fromstring(img_data, np.uint8)
#             pic = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#             detector = PoseDetector()

#             pic = detector.findPose(pic)
#             lmListpic, bboxInfopic = detector.findPosition(pic, bboxWithHands=False)
#             print(lmListpic)
#             lmp11 = lmListpic[11][1:3]
#             lmp12 = lmListpic[12][1:3]
#             lmp24 = lmListpic[24][1:3]
#             lmp23 = lmListpic[23][1:3]
#             cv2.imshow("Picture",pic)
#             cv2.waitKey(0)

#             img = cv2.imread("Resources/Shirts/3.png")
#             img = detector.findPose(img)
#             lmListShirt, bboxInfoShirt = detector.findPosition(img, bboxWithHands=False)
#             print(lmListShirt)
#             lms11 = lmListShirt[11][1:3]
#             lms12 = lmListShirt[12][1:3]
#             lms24 = lmListShirt[24][1:3]
#             lms23 = lmListShirt[23][1:3]
#             cv2.imshow("Shirt",img)
#             cv2.waitKey(0)

#             orgwidth =int(lms11[0] - lms12[0])
#             orgheight =int(lms11[1] - lms23[1])
#             widthOfShirt = int(orgwidth * (int(lmp11[0]-lmp12[0])/orgwidth))
#             heightOfShirt = int(orgheight * (int(lmp11[1]-lmp23[1])/orgheight))
#             if(widthOfShirt<0):
#                 widthOfShirt=widthOfShirt*(-1)
#             if(heightOfShirt<0):
#                 heightOfShirt=heightOfShirt*(-1)
#             img = cv2.resize(img,(widthOfShirt,heightOfShirt))
#             cv2.imshow('Resized Image',img)
#             cv2.waitKey(0)
#         except Exception as e:
#              print(e)
#              return Response({'message': 'Error'})
        

class LoginAPI(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data = data)
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']

                user = authenticate(email = email, password = password)

                if user is None:
                    return Response({
                    'status' : 400,
                    'message' : 'Invalid password',
                    'data' : {},
                })

                refresh = RefreshToken.for_user(user)

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })


            return Response({
                    'status' : 400,
                    'message' : 'something went wrong',
                    'data' : serializer.errors,
                })
        
        except Exception as e:
            print(e)
                
            



# class RegisterAPI(APIView):

#     def post(self, request):
#         try:
#             data = request.data
#             serializer = CustomUserSerializer(data = data)
#             if serializer.is_valid(raise_exception=True):
#                 user = serializer.save()
#                 send_otp_via_email(user.email)
#                 return Response({
#                     'status' : 200,
#                     'message' : 'registration successful....check email',
#                     'data' : serializer.data,
#                 })
            
#             return Response({
#                     'status' : 400,
#                     'message' : 'something went wrong',
#                     'data' : serializer.errors,
#                 })
        
#         except Exception as e:
#             print(e)

class RegisterAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = CustomUserSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                send_otp_via_email(user.email)
                return Response({
                    'status': 200,
                    'message': 'Registration successful... Check your email',
                    'data': serializer.data,
                })

            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': serializer.errors,
            })

        except Exception as e:
            print(e)



class VerifyOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data = data)
            if serializer.is_valid(raise_exception=True):
                email = serializer.data['email']
                otp = serializer.data['otp']

                user = CustomUser.objects.filter(email = email)
                if not user.exists():
                    return Response({
                    'status' : 400,
                    'message' : 'something went wrong',
                    'data' : 'invalid email',
                })

                if user[0].otp != otp:
                    return Response({
                    'status' : 400,
                    'message' : 'something went wrong',
                    'data' : 'wrong otp',
                })

                user = user.first()
                user.is_verified = True
                user.save()

                return Response({
                    'status' : 200,
                    'message' : 'account verified',
                    'data' : {},
                })

        except Exception as e:
            print(e)















    



