// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

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
const auth = getAuth(app);

export { app, auth };