pipeline {
    agent any

    environment {
        AWS_URL = '352708296901.dkr.ecr.eu-west-2.amazonaws.com'
    }

    stages {
        stage('Artifactory config'){
        steps{
            rtServer (
                id: 'Artifactory-1',
                url: 'http://my-artifactory-domain/artifactory',
                // If you're using username and password:
//                 username: 'user',
//                 password: 'password',
                // If you're using Credentials ID:
                credentialsId: 'ccrreeddeennttiiaall',
                // If Jenkins is configured to use an http proxy, you can bypass the proxy when using this Artifactory server:
                bypassProxy: true,
                // Configure the connection timeout (in seconds).
                // The default value (if not configured) is 300 seconds:
                timeout: 300
            )
        }

        }

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
            post {
                 always {
                     // previous to version 2.0.0 you must provide parameters to this command (see below)!
                     jiraSendBuildInfo()
                 }
             }
        }
        stage('Test') {
            when {
                anyOf {
                        branch 'master'
                        branch 'dev'
                    }

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
            parallel{
                stage('Stage 1') {
                    steps {
                        echo 'step1'
                        sh '''
                            aws eks update-kubeconfig --region eu-west-2 --name cicd-mar22-k8s
                            IMAGE_NAME=flask-app-yoan:0.0.${BUILD_ID}
                            sed -i "s/{{AWS_URL}}/$AWS_URL/g" ./k8s/simple-web-server.yaml
                            sed -i "s/{{IMAGE_NAME}}/$IMAGE_NAME/g" ./k8s/simple-web-server.yaml
                            kubectl apply -f ./k8s/simple-web-server.yaml
                        '''
                    }
                }
                stage('Stage 2') {
                    steps {
                        echo 'step2'
                     }
                     post {
                        always {
                            jiraSendDeploymentInfo environmentId: 'us-prod-1', environmentName: 'us-prod-1', environmentType: 'production'
                        }
                    }
                }
            }
       }
    }
}