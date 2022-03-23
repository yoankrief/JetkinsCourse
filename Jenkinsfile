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
                sh 'printenv'
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
                anyOf {
                        branch 'master'
                        branch 'dev'
                    }

                //changeRequest target: 'dev'

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
                sh '''
                    aws eks update-kubeconfig --region eu-west-2 --name cicd-mar22-k8s
                    REGISTRY_URL=${AWS_URL}//flask-app-yoan:0.0.${BUILD_ID}
                    sed -i "s/{{REGISTRY_URL}}/$REGISTRY_URL/g" ./k8s/simple-web-server.yaml
                    kubectl apply -f ./k8s/simple-web-server.yaml


                '''
            }
        }
    }
}