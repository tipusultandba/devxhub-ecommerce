pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = '5de11ef2-cad3-4e3f-a2ae-288b5b58cbfb'  // Jenkins credentials ID for Docker Hub
        DOCKER_IMAGE_NAME = 'tipu247/ecommerce'
        DOCKER_IMAGE_TAG = 'latest'
        DOCKER_REGISTRY = 'https://index.docker.io/v1/'
        DEPLOY_PATH = "/var/www/html/devxhub-ecommerce/"
        SSH_USER = "deploy"
        DEPLOY_SERVER = "192.168.126.143"
    }

    stages {
        stage('Checkout') {
            steps {
                // Pull the code from the Git repository
                git branch: 'main', credentialsId: '3e711f9d-ea7a-49fd-9a5a-fd9c17a32f3d', url: 'https://github.com/Iqbalkhan319/devxhub-ecommerce.git'
            }
        }

        stage('Change env') {
            steps {
                script {
                    sh '''
                    echo "Updating .env file with Jenkins environment variables..."
                    cp .env.example .env
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image
                    docker.build("${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}")
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    // Log in to Docker Hub using Jenkins credentials
                    docker.withRegistry(DOCKER_REGISTRY, DOCKER_CREDENTIALS_ID) {
                        echo 'Logged in to Docker Hub successfully!'
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Push the Docker image to Docker Hub
                    docker.withRegistry(DOCKER_REGISTRY, DOCKER_CREDENTIALS_ID) {
                        docker.image("${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}").push()
                    }
                }
            }
        }
        stage('Approval') {
            steps {
                input "Do you approve this build?"
            }
        }
        stage('Deploy to Server') {
            steps {
                script {
                    // Use Jenkins credentials for Docker Hub login in the remote server
                    withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_HUB_USER', passwordVariable: 'DOCKER_HUB_PASSWORD')]) {
                        // SSH into the server and deploy the app using Docker Compose
                        sh """
                        ssh ${SSH_USER}@${DEPLOY_SERVER} 'sudo mkdir -p ${DEPLOY_PATH} && sudo chown -R ${SSH_USER}. ${DEPLOY_PATH}'
                        rsync -avhP -e "ssh -o StrictHostKeyChecking=no" --exclude '.git/' . ${SSH_USER}@${DEPLOY_SERVER}:${DEPLOY_PATH}
                        ssh ${SSH_USER}@${DEPLOY_SERVER} <<EOF
cd ${DEPLOY_PATH}
echo "${DOCKER_HUB_PASSWORD}" | docker login -u "${DOCKER_HUB_USER}" --password-stdin
docker compose pull
docker compose down
docker compose up -d --remove-orphans
EOF
                        """
                    }
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    // Remove local Docker images to save space
                    sh "docker rmi ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
                }
            }
        }
    }

    post {
        success {
            echo 'UAT deployment successful!'
            mail to: 'tipu.brcp1@gmail.com',
                 from: 'tipu.idea2@gmail.com',
                 subject: "UAT Pipeline Success: ${currentBuild.fullDisplayName}",
                 body: "UAT deployment successful for build ${env.BUILD_NUMBER}.\nView console output at ${env.BUILD_URL}"
        }

        failure {
            echo 'UAT deployment failed!'
            emailext attachLog: true,  // Attach the build log to the email
                    to: 'tipu.brcp1@gmail.com',
                    from: 'tipu.idea2@gmail.com',
                    subject: "UAT Pipeline Failure: ${currentBuild.fullDisplayName}",
                    body: "UAT deployment failed for build ${env.BUILD_NUMBER}.\nView console output at ${env.BUILD_URL}"
        }
        always {
            // Clean up workspace after build
            cleanWs()
        }
    }
}
