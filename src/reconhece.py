#Salve este arquivo com o nome 'reconhece.py' para funcionar corretamente com os outros dois.
import sympy as sp  #Você deve ter o sympy instalado corretamente.

def Reconhecer_conicas(A, B, C, D, E, F):
    # Matrizes para cálculo de determinantes
    M = sp.Matrix([[sp.Rational(A), sp.Rational(B,2), sp.Rational(D,2)], 
                    [sp.Rational(B,2), sp.Rational(C), sp.Rational(E,2)], 
                    [sp.Rational(D,2), sp.Rational(E,2), sp.Rational(F)]])
    M1 = sp.Matrix([[sp.Rational(A), sp.Rational(B,2)], 
                     [sp.Rational(B,2), sp.Rational(C)]])

    # Invariantes
    delta1 = A + C 
    delta2 = M1.det() 
    delta3 = M.det() 

    tol = 1e-9    #Definimos um grau de tolerância para evitar confusões do programa.
#PARTE I - Reconhecendo cônicas com sistemas de ifs usando os invariantes:
    if abs(delta3) > tol: 
        if abs(delta2) > tol:
            if delta2 > 0:
                if abs(A - C) < tol and abs(B) < tol:
                    return "Circunferência"
                else:
                    return "Elipse"
            else: # delta2 < 0
                return "Hipérbole"
        else: # delta2 == 0
            return "Parábola"
    else: # Cônicas degeneradas (delta3 == 0)
        if abs(delta2) > tol: 
            if delta2 > 0: 
                return "Ponto Degenerado" 
            else: # delta2 < 0 
                return "Duas Retas que se Cruzam" 

        else: # delta2 == 0 e delta3 == 0 (Parábolas degeneradas)
            if abs(C) < tol and abs(B) < tol and abs(E) < tol: 
                if all(abs(val) < tol for val in [A, D, F]):
                    return "Plano Inteiro (0=0)"
                
                discriminante = D**2 - 4 * A * F
                if abs(discriminante) < tol:
                    return "Reta Dupla"
                elif discriminante > 0:
                    return "Duas Retas Paralelas"
                else: 
                    return "Conjunto Vazio"
            
            if abs(A) < tol and abs(B) < tol and abs(D) < tol: 
                if all(abs(val) < tol for val in [C, E, F]):
                    return "Plano Inteiro (0=0)"
                
                discriminante = E**2 - 4 * C * F
                if abs(discriminante) < tol:
                    return "Reta Dupla"
                elif discriminante > 0:
                    return "Duas Retas Paralelas"
                else: 
                    return "Conjunto Vazio"
            
            if abs(A) < tol and abs(C) < tol and abs(B) > tol:
                return "Duas Retas que se Cruzam" 

            return "Caso Degenerado Indefinido"

#PARTE II- Simplificando a equação geral utilizando diagonalização de matrizes.
def simplificar(a, b, c, d, e, f):
    x, y = sp.symbols('x y')
    eq = sp.Rational(a) * x**2 + sp.Rational(b) * x * y + sp.Rational(c) * y**2 + sp.Rational(d) * x + sp.Rational(e) * y + sp.Rational(f)
    
    tipo = Reconhecer_conicas(a, b, c, d, e, f)  
    
    sp.pprint(eq)

    if tipo in ["Ponto Degenerado", "Duas Retas que se Cruzam", "Reta Dupla", 
                "Duas Retas Paralelas", "Conjunto Vazio", "Plano Inteiro (0=0)",
                "Caso Degenerado Indefinido"]:
        return [tipo]

    x1, y1 = sp.symbols('x1 y1') 
    x2, y2 = sp.symbols('x2 y2') 

    eq_finalizada = eq 
    tol = 1e-9 

    # 1. Rotação se B != 0
    if abs(b) > tol: 
        M_quad = sp.Matrix([[sp.Rational(a), sp.Rational(b,2)], 
                             [sp.Rational(b,2), sp.Rational(c)]])
        
        autovetores_dict = M_quad.eigenvects()
        
        v1 = autovetores_dict[0][2][0].normalized()
        v2 = autovetores_dict[1][2][0].normalized()
        
        U = sp.Matrix([[v1[0], v2[0]], [v1[1], v2[1]]])
        
        eq_rotacionada = eq.subs({x: U[0,0]*x1 + U[0,1]*y1, 
                                  y: U[1,0]*x1 + U[1,1]*y1}).expand()
        eq_rotacionada = sp.simplify(eq_rotacionada)

        
        sp.pprint(eq_rotacionada)
        
        
        eq_finalizada = eq_rotacionada
        
    else: 
        eq_finalizada = eq.subs({x:x1, y:y1})

    # 2. Translação (Completar o quadrado)
    sqr_x_term_sym = eq_finalizada.coeff(x1**2)
    sqr_y_term_sym = eq_finalizada.coeff(y1**2)
    lin_x_term_sym = eq_finalizada.coeff(x1) 
    lin_y_term_sym = eq_finalizada.coeff(y1) 

    trans_x = sp.S.Zero
    trans_y = sp.S.Zero

    if not sqr_x_term_sym.is_zero and not lin_x_term_sym.is_zero:
        trans_x = -lin_x_term_sym / (2 * sqr_x_term_sym) 
    
    if not sqr_y_term_sym.is_zero and not lin_y_term_sym.is_zero:
        trans_y = -lin_y_term_sym / (2 * sqr_y_term_sym)

    eq_finalizada = eq_finalizada.subs({x1: x2 + trans_x, y1: y2 + trans_y}).expand()
    eq_finalizada = sp.simplify(eq_finalizada)


    sp.pprint(eq_finalizada)
    

    # 3. Normalização para forma canônica
    final_const_sym = eq_finalizada.coeff(x2, 0).coeff(y2, 0)
    
    if abs(final_const_sym.evalf()) < tol: 
        # Baseado no tipo original, retorna o degenerado correto
        if tipo == 'Elipse' or tipo == 'Circunferência':
            return ["Ponto Degenerado"]
        elif tipo == 'Hipérbole':
            return ["Duas Retas que se Cruzam"]
        elif tipo == 'Parábola':
            # Parábola degenerada com constante zero pode ser reta dupla
            coeff_x2_sq = eq_finalizada.coeff(x2**2)
            coeff_y2_sq = eq_finalizada.coeff(y2**2)
            if not coeff_x2_sq.is_zero or not coeff_y2_sq.is_zero:
                 return ["Reta Dupla"]
            else:
                 return ["Caso Degenerado Indefinido"] # Se não sobrou termo quadrático, é mais complexo

    # Remove a constante para ter apenas os termos quadráticos/lineares que serão normalizados
    eq_to_normalize = eq_finalizada - final_const_sym

    # Normaliza a equação para que o lado direito seja 1 ou -1
    eq_normalized = eq_to_normalize / (-final_const_sym) 
    eq_normalized = sp.simplify(eq_normalized) 

    
    sp.pprint(eq_normalized)
    

    if tipo in ['Elipse', 'Circunferência']:
        x2_coeff_val = eq_normalized.coeff(x2**2)
        y2_coeff_val = eq_normalized.coeff(y2**2)

        if x2_coeff_val.is_zero or x2_coeff_val.is_negative:
            return ["Conjunto Vazio"]
        
        if y2_coeff_val.is_zero or y2_coeff_val.is_negative:
            return ["Conjunto Vazio"]

        eixo_x_val = sp.sqrt(1 / x2_coeff_val).evalf()
        eixo_y_val = sp.sqrt(1 / y2_coeff_val).evalf()

        eixo_maior = max(eixo_x_val, eixo_y_val)
        eixo_menor = min(eixo_x_val, eixo_y_val)
        
        if abs(eixo_maior - eixo_menor) < tol:
            tipo = 'Circunferência'
            valores = [tipo, eixo_maior]
        else:
            valores = [tipo, eixo_maior, eixo_menor]
        return valores

    elif tipo == 'Hipérbole':
        x2_coeff_val = eq_normalized.coeff(x2**2)
        y2_coeff_val = eq_normalized.coeff(y2**2)

        # Para hipérboles, um dos coeficientes quadráticos deve ser positivo e o outro negativo
        if (sp.sign(x2_coeff_val) != sp.sign(y2_coeff_val) and not x2_coeff_val.is_zero and not y2_coeff_val.is_zero):
            eixo_real = sp.sqrt(abs(1 / x2_coeff_val)).evalf()
            eixo_imaginario = sp.sqrt(abs(1 / y2_coeff_val)).evalf()
            
            valores = [tipo, eixo_real, eixo_imaginario]
            return valores
        else:
            # Isso não deveria ser atingido se já classificamos como hipérbole não degenerada
            # Mas serve como um fallback de segurança
            return ["Duas Retas que se Cruzam"]
    
    elif tipo == 'Parábola':
        coeff_x2_sq = eq_normalized.coeff(x2**2) 
        coeff_y2_sq = eq_normalized.coeff(y2**2)
        coeff_x2_lin = eq_normalized.coeff(x2)
        coeff_y2_lin = eq_normalized.coeff(y2)

        if not coeff_x2_sq.is_zero and coeff_y2_sq.is_zero: 
            if not coeff_y2_lin.is_zero:
                p_val = -(coeff_y2_lin / coeff_x2_sq).evalf() / 4
                return [tipo, p_val]
            else: # x2^2 existe, mas termo linear em y2 é zero (degenerada)
                return ["Reta Dupla"] if final_const_sym.is_zero else ["Conjunto Vazio"]
        
        elif not coeff_y2_sq.is_zero and coeff_x2_sq.is_zero: 
            if not coeff_x2_lin.is_zero:
                p_val = -(coeff_x2_lin / coeff_y2_sq).evalf() / 4
                return [tipo, p_val]
            else: # y2^2 existe, mas termo linear em x2 é zero (degenerada)
                return ["Reta Dupla"] if final_const_sym.is_zero else ["Conjunto Vazio"]

        return ["Caso Degenerado Indefinido"] 

    return [tipo]
