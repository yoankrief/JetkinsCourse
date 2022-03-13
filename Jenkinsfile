pipeline {
    agent any

    environment {
        AWS_URL = '352708296901.dkr.ecr.eu-west-2.amazonaws.com'
    }

    stages {
        stage('Build') {
            when {
                anyOf {
                    branch 'master'
                    branch 'dev'
                }
            }
            steps {
                sh '''
                cd simple_webserver
                aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin ${AWS_URL}
                docker build -t flask-app-yoan .
                docker tag flask-app-yoan:latest ${AWS_URL}/flask-app-yoan:0.0.${BUILD_ID}
                docker push ${AWS_URL}/flask-app-yoan:0.0.${BUILD_ID}
                '''
            }
        }
        stage('Test') {
        //when {changeRequest()}
            steps {
                echo JOB_NAME
                sh '''
                    cd simple_webserver
                    pip3 install -r requirements.txt
                    PYTHONPATH=. python3 -m pytest --junitxml results.xml ./tests
                '''
            }
        }
        stage('Deploy') {
            steps {
                echo 'Finally deploying...'
            }
        }
    }
}