pipeline {
    agent any


    stages {
        stage('Build') {
            when {
                branch 'master'
            }
            steps {
                echo 'I am building ... '
                echo BUILD_ID
                sh '''
                aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 352708296901.dkr.ecr.eu-west-2.amazonaws.com
                docker build -t flask-app-yoan .
                docker tag flask-app-yoan:latest 352708296901.dkr.ecr.eu-west-2.amazonaws.com/flask-app-yoan:latest
                docker push 352708296901.dkr.ecr.eu-west-2.amazonaws.com/flask-app-yoan:latest
                '''
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