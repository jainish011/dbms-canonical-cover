import streamlit as st
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
    .css-fg4pbf {
    position: absolute;
    background: #2F5233;
    inset: 0px;
    overflow: hidden;
    font-family: 'Montserrat', sans-serif;
}
h1 {
    font-family: 'Montserrat', sans-serif;
    font-weight: 700;
    color: #ECF87F;
    padding: 1.25rem 0px 1rem;
    margin: 0px;
    line-height: 1.4;
}
.css-qrbaxs {
    font-family: 'Montserrat', sans-serif;
    font-size: 20px;
    color: #B1D8B7;
    margin-bottom: 7px;
    height: auto;
    min-height: 1.5rem;
    vertical-align: middle;
    display: flex;
    flex-direction: row;
    -webkit-box-align: center;
    align-items: center;
}
.css-12ttj6m {
    font-family: 'Montserrat', sans-serif;
    border: none
    border-radius: 0.25rem;
    padding: calc(1em - 1px);
}
.css-1n76uvr {
    font-family: 'Montserrat', sans-serif;
    width: 750px;
    position: relative;
    display: flex;
    flex: 1 1 0%;
    flex-direction: column;
    gap: 1.5rem;
}
p, ol, ul, dl {
    
    font-family: 'Montserrat', sans-serif;
    margin: 1px 1px 1rem;
    padding: calc(1em - 1px);
    font-size: 1.2rem;
    font-weight: 500;
    COLOR: #2f5233;
    background-color: #acd3b2;
    border-radius:10px
}
.css-10trblm {
    font-family: 'Montserrat', sans-serif;
    position: relative;
    flex: 1 1 0%;
    margin-left:4rem;
    color: #ECF87F;
}
.css-qrbaxs {
    font-family: 'Montserrat', sans-serif;
    font-weight:500;
}
.css-183lzff {
    
    font-family: 'Montserrat', sans-serif;S
    white-space: pre;
    font-size: 14px;
    overflow-x: auto;
    color:#ff5555;
    font-weight:600;
}
.css-1cpxqw2 {
    font-family: 'Montserrat', sans-serif;
    display: inline-flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 500;
    padding: 0.25rem 0.75rem;
    border-radius: 0.25rem;
    margin: 0px;
    line-height: 1.6;
    color: #030b00;
    width: auto;
    user-select: none;
    background-color: #94C973;
}
.css-1cpxqw2:hover {
    box-shadow:0px 0px 5px 1px black;
    color: #030b00;
    border:none;
}
.css-1cpxqw2:focus:not(:active) {
     border-color:black 
     color: #030b00;
}
.st-ck{
    border-bottom-color:black;
}
.st-cj{
    border-top-color:black;
}
.st-ci{
    border-right-color:black;
}
.st-ch{
    border-left-color:black;
}
    </style>
    """,
    unsafe_allow_html=True
)
st.title("CANONICAL COVER")
with st.form("my_form"):
    # st.write("Inside the form")
    # slider_val = st.slider("Form slider")
    # checkbox_val = st.checkbox("Form checkbox")
    rSchema=st.text_input("Enter Relational Schema:",placeholder='Example: R(A,B,C,D,E)')
    list = st.text_input("Enter Functional dependencies:", "",placeholder='Example: A->B,B->C,C->D')
    rSchema=rSchema[2:len(rSchema)-1].split(',')
    print(rSchema)
    submitted = st.form_submit_button("Submit")
    flag=0
    error=''
    for s in list:
        if(s==',' or s=='-' or s=='>'):
            continue
        else:
            if(s not in rSchema):
                error=s
                flag=1
    if(flag==1):
        st.text(f'{error} is not present in relational schema!!')

    if(rSchema=='' or list=='' and submitted):
        st.text(f'Text input should not be empty!!')

if st.button('Run'):
    list = list.split(",")
    # st.markdown(f"{list}")
    def decomposition(list):
        for l in list:
            for l in list:
                tuple=l.split('->')
                right=tuple[1]
                if len(right)>1:
                    st.write(f"{l} will decompose into:")
                    for i in range(len(right)):
                        a=tuple[0]+"->"+right[i]
                        st.write(a,end=', ')
                        list.append(a)
                    st.write('\n')
                    list.remove(l)
        st.write('\n')
        return list

    def findClosure(list,a):
        cl=[]
        for i in range(len(a)):
            cl.append(a[i])   
        for l in list:
            for l in list:
                tuple=l.split('->')
                flag=0
                left=tuple[0]
                for i in range(len(left)):
                    if left[i] not in cl:
                        flag=1
                if flag==0 and tuple[1] not in cl:
                    cl.append(tuple[1])
        return cl

    def removeExtraFD(list):
        flag=0
        for l in list:
            for l in list:
                tuple=l.split('->')
                temp=list.copy()
                temp.remove(l)
                if(sorted(findClosure(temp,tuple[0]))==sorted(findClosure(list,tuple[0]))):
                    #st.write("Here ",l," is extra functional dependency because closure of ", tuple[0]," with right attributes and closure of ", tuple[0], " without right attribute is same")
                    st.write(f"Here {l} is extra functional dependency because closure of {tuple[0]} with right attributes and closure of {tuple[0]} without right attribute is same.\n")
                    flag=1      
                    list.remove(l)
        if(flag==0):
            st.write("There is no extra functional dependency in this list.\n")
        return list

    def removeChar(str,a):
        temp=""
        for i in range(len(str)):
            if i!=a:
                temp=temp+str[i]
        return temp

    def removeExtraAttribute(list):
        flag=0
        for l in list:
            tuple=l.split('->')
            left=tuple[0]
            if len(left)>1:
                for i in range(len(left)):
                    temp_str=removeChar(left,i)
                    a=temp_str+"->"+tuple[1]
                    if((left[i] in findClosure(list,temp_str)) and (l in list)):
                        st.write(f'In {l} functional dependency attribute {left[i]} is extra attribute.')
                        st.write(f'Because {left[i]} is present in the closure of {a} and closure of {a} is {findClosure(list,temp_str)}')
                        list.append(a)
                        list.remove(l)
                        flag=1
        if flag==0:
            st.write('There is no functional depedency with extra attributes\n')
        return list

    def add(list):
        str=""
        tuple=""
        for i in range(len(list)):
            tuple=list[i].split('->')
            str+=tuple[1]
        a=tuple[0]+"->"+str
        return a

    def composition(list):
        for i in list:
            tuple1=i.split('->')
            temp=[]
            for j in list:
                tuple2=j.split('->')
                if(tuple1[0]==tuple2[0] and (j not in temp)):
                    temp.append(j)
            
            if len(temp)>1:
                for t in temp:
                    list.remove(t)
                a=add(temp)
                list.append(a)
        
        return list

    st.header("Steps for canonical cover:")

    st.write(f"Main Functional Dependency List: {list}\n")

    st.subheader('Step-1: Decomposition')
    st.write("In this step we decompose all our functional depedency.")
    list=decomposition(list) 
    st.write(f"Functional dependency list after step-1:\n{list}\n")


    st.subheader('Step-2: Remove Extra Functional Dependency.')
    list=removeExtraFD(list) 
    st.write(f"Functional Dependency list after step-2: {list}\n")

    st.subheader('Step-3: Remove Extra Attributes from functional dependency\n')
    list=removeExtraAttribute(list)
    st.write(f"Functional Dependency list after step-3: {list}\n")
    list=composition(list)

    st.subheader('Final Step: Compostion')
    st.write('In this step we will compose all our functional dependency.')

    st.write(f"After Composition here is functional dependency list: {list}\n")