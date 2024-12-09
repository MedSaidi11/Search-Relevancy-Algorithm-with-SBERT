pipeline {
    agent any
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
                withCredentials([
                    usernamePassword(
                        credentialsId: 'INSTANCE_ID', 
                        usernameVariable: 'INSTANCE_ID', 
                        passwordVariable: 'EC2_INSTANCE_ID'
                    ),
                    usernamePassword(
                        credentialsId: 'AWS_REGION', 
                        usernameVariable: 'AWS_REGION', 
                        passwordVariable: 'AWS_REGION'
                    ),
                    usernamePassword(
                        credentialsId: 'AWS_ACCESS_KEY', 
                        usernameVariable: 'AWS_ACCESS_KEY_ID', 
                        passwordVariable: 'AWS_ACCESS_KEY_ID'
                    ),
                    usernamePassword(
                        credentialsId: 'SECRET-ACCESS_KEY', 
                        usernameVariable: 'SECRET-ACCESS_KEY', 
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ])
                script {
                    // Use AWS CLI to restart EC2 instance
                    sh """
                        echo "Rebooting EC2 instance with ID: $EC2_INSTANCE_ID in region: $AWS_REGION"
                        aws ec2 reboot-instances --instance-ids $EC2_INSTANCE_ID --region $AWS_REGION
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
