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
            when {
                changeRequest target: 'dev'

            }
            steps {
                echo JOB_NAME
                sh 'printenv'
                sh '''
                    pip3 install -r simple_webserver/requirements.txt
                    PYTHONPATH=. python3 -m pytest --junitxml results.xml simple_webserver/tests
                '''
            }

            post {
                always{
                    junit allowEmptyResults: true, testResults: 'results.xml'
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Finally deploying...'
            }
        }
    }
}