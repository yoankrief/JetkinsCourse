pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'I am building ... '
                echo BUILD_ID
            }
        }
        stage('Test') {
            steps {
                echo 'I am testing... '
                echo JOB_NAME
            }
        }
        stage('Deploy') {
            steps {
                echo 'Finally deploying...'
            }
        }
    }
}