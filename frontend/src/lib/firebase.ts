import { initializeApp } from 'firebase/app'
import { 
  getAuth, 
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signInWithPopup,
  GoogleAuthProvider,
  sendEmailVerification,
  signOut as firebaseSignOut,
  onAuthStateChanged,
  User
} from 'firebase/auth'

// Firebase configuration (from user's provided config)
const firebaseConfig = {
  apiKey: "AIzaSyDCtNeHZXL4dDBSumv-mNUsUxlsm21v1SM",
  authDomain: "matrix-f7b56.firebaseapp.com",
  projectId: "matrix-f7b56",
  storageBucket: "matrix-f7b56.firebasestorage.app",
  messagingSenderId: "856049900375",
  appId: "1:856049900375:web:6631c27cc3d37099583c12",
  measurementId: "G-2D29TE3K1M"
}

// Initialize Firebase
const app = initializeApp(firebaseConfig)
const auth = getAuth(app)
const googleProvider = new GoogleAuthProvider()

export {
  auth,
  googleProvider,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signInWithPopup,
  sendEmailVerification,
  signOut: firebaseSignOut,
  onAuthStateChanged,
  User
}