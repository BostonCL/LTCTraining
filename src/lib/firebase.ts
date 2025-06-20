// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAJlljC-nxM6TItEIEu4sOVxGmf7DQYPO8",
  authDomain: "ltctraining.firebaseapp.com",
  projectId: "ltctraining",
  storageBucket: "ltctraining.firebasestorage.app",
  messagingSenderId: "632518354840",
  appId: "1:632518354840:web:00204eab3e14b0b6f3aded"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export { app };