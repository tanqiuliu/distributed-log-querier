export NODE=(fa18-cs425-g45-01.cs.illinois.edu \
fa18-cs425-g45-02.cs.illinois.edu \
fa18-cs425-g45-03.cs.illinois.edu \
fa18-cs425-g45-04.cs.illinois.edu \
fa18-cs425-g45-05.cs.illinois.edu \
fa18-cs425-g45-06.cs.illinois.edu \
fa18-cs425-g45-07.cs.illinois.edu \
fa18-cs425-g45-08.cs.illinois.edu \
fa18-cs425-g45-09.cs.illinois.edu \
fa18-cs425-g45-10.cs.illinois.edu)

export USER=tanqiul2

# for i in ${NODE[@]}
# do 
# ssh $USER@$i "rm /home/$USER/.ssh/known_hosts"
# done


echo "remvoe key on "
rm /home/$USER/.ssh/id_rsa
echo "generate key on "
ssh-keygen -f /home/$USER/.ssh/id_rsa -t rsa -N ''
for j in ${NODE[@]}
do
echo "make connection to $j"
# ssh -o StrictHostKeyChecking=no $USER@$i "cat /home/$USER/.ssh/id_rsa.pub" | ssh -o StrictHostKeyChecking=no $USER@$j 'cat >> .ssh/authorized_keys'
ssh-copy-id -o StrictHostKeyChecking=no -i /home/$USER/.ssh/id_rsa $USER@$j
done

