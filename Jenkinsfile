pipeline {
    agent { //agent any does not allow specifying the custom workspace
        node
        {
            label 'local'
            customWorkspace 'D:\\Departmental Data\\Subjects Data\\July-Dec 2025\\MLOPs\\CICD\\Demo1_Jenkins_as_Container' /*as our project is not at the standard path*/
        }
    }
    stages {
 /*
 stage('Checkout Code') {
 steps {
 git branch: 'main', url: 'https://github.com/your-username/iris_project.git'
 }
 }*/
 stage('Show Workspace') {
 steps {
 bat 'cd’  #prints CWD
 }
 }
A Sample Jenkins file
 stage('Build Im