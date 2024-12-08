pipeline {
    agent any

    environment {
        EC2_INSTANCE_ID = credentials('instance-id') 
        AWS_REGION = credentials('aws-region')          
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
    }

    triggers {
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'prod', url: 'https://github.com/yourusername/yourrepository.git'
            }
        }

        stage('Restart EC2 Instance') {
            steps {
                script {
                    // Use AWS CLI to restart EC2 instance
                    sh """
                        aws ec2 reboot-instances --instance-ids ${EC2_INSTANCE_ID} --region ${AWS_REGION}
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                        docker-compose build
                    """
                }
            }
        }

        stage('Deploy Docker Container') {
            steps {
                script {
                    sh """
                        docker-compose up
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo 'Build and deployment successful.'
        }
        failure {
            echo 'There was a failure in the pipeline.'
        }
    }
}
