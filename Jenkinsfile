pipeline {
    agent any

    environment {
        AWS_URL = '352708296901.dkr.ecr.eu-west-2.amazonaws.com'
        PATH = "./venv/bin:$PATH"
    }

    stages {
        stage('Create venv'){
        steps {
                sh '''
                    python3 -m venv ./venv
                    #source ./venv/bin/activate
                '''
            }
        }

        stage('Artifactory config'){
            steps{
                rtServer (
                    id: 'artifactory-yoan',
                    url: 'https://yoankrief.jfrog.io/artifactory',
                    credentialsId: 'jfrog-secret',
                )

                rtPipResolver (
                    id: "pip-default",
                    serverId: "artifactory-yoan",
                    repo: "dependencies-pypi"
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
                rtPipInstall (
                    resolverId: "pip-default",
                    args: "-r simple_webserver/requirements.txt",
                )


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
                    ./venv/bin/pip install -r simple_webserver/requirements.txt
                    PYTHONPATH=. ./venv/bin/python -m pytest --junitxml results.xml simple_webserver/tests
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
                            #aws eks update-kubeconfig --region eu-west-2 --name cicd-mar22-k8s
                            #IMAGE_NAME=flask-app-yoan:0.0.${BUILD_ID}
                            #sed -i "s/{{AWS_URL}}/$AWS_URL/g" ./k8s/simple-web-server.yaml
                            #sed -i "s/{{IMAGE_NAME}}/$IMAGE_NAME/g" ./k8s/simple-web-server.yaml
                            #kubectl apply -f ./k8s/simple-web-server.yaml
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

       stage ('Package and create distribution archives') {
            steps {
                sh '''
                    ./venv/bin/pip install wheel
                    cd package_demo
                    ../venv/bin/python setup.py sdist bdist_wheel
                '''
            }
        }

        stage ('Package publish') {
            steps {
                rtUpload (
                    serverId: 'artifactory-yoan',
                    spec: '''{
                          "files": [
                            {
                              "pattern": "package_demo/dist/",
                              "target": "fantastic-pypi/"
                            }
                         ]
                    }'''


                )
            }
        }
    }
}