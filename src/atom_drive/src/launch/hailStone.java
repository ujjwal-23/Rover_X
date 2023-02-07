import java.util.*;

interface Number1{

    public boolean checknumber(int a);

    public int odd(int a);

    public int even(int a);

}

 

public class hailStone implements Number1

{

    public boolean checknumber(int n){

        if(n%2==0){

            return false;

        }

        else{

            return true;

        }

    }

    public int odd(int a){

        return a*3+1;

    }

    public int even(int b){

        return (b/2);

    }

public static void main(String[] args) {

    hailStone hs=new hailStone();

    Scanner sc=new Scanner(System.in);

    int n=sc.nextInt();

    int count=1;

    System.out.print(n+" ");

    while(n!=1){

        if(hs.checknumber(n)){

            n=hs.odd(n);

            System.out.print(n+" ");

        }else{

            n=hs.even(n);

            System.out.print(n+" ");

        }

       count+=1;

    }

    System.out.println();

    System.out.println("The number of elements in the sequence are "+count);

}

}

