pipeline {
    agent any

    environment {
        EC2_INSTANCE_ID = "i-0d973c9e41d4061d0"
        AWS_REGION = "us-east-1"      
        AWS_ACCESS_KEY_ID = "AKIA2UC27Y42QN3TEQI5"
        AWS_SECRET_ACCESS_KEY = "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"
    }

    triggers {
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'prod', url: 'https://github.com/MedSaidi11/Semantic-Search-Engine-using-Sentence-BERT.git'
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
